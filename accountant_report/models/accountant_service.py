# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import (  # pylint: disable=redefined-builtin
    safe_eval as eval,
)
from openerp.tools.translate import _


class AccountantService(models.Model):
    _inherit = "accountant.service"

    # TODO: Here or other module?
    service_code = fields.Char(
        string="Code",
    )
    sequence_creation_method = fields.Selection(
        string="Sequence Creation Method",
        selection=[
            ("standard", "Standard"),
            ("code", "Python Code"),
        ],
        required=True,
        default="standard",
    )
    sequence_python_code = fields.Text(
        string="Python Code for Custom Sequence Generation",
    )
    allowed_opinion_ids = fields.Many2many(
        string="Allowed Opinion",
        comodel_name="accountant.report_opinion",
        relation="rel_accountant_service_2_opinion",
        column1="service_id",
        column2="opini_id",
    )
    allowed_method_ids = fields.Many2many(
        string="Allowed Methods",
        comodel_name="accountant.report_method",
        relation="rel_accountant_service_2_method",
        column1="method_id",
        column2="opini_id",
    )
    opinion_required = fields.Boolean(
        string="Opinion Required",
    )
    method_required = fields.Boolean(
        string="Method Required",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    signing_accountant_ids = fields.One2many(
        string="Signing Partner",
        comodel_name="accountant.report_signing_partner",
        inverse_name="service_id",
    )
    confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm",
        comodel_name="res.groups",
        relation="rel_accountant_service_allowed_confirm_groups",
        column1="service_id",
        column2="group_id",
    )
    finalize_grp_ids = fields.Many2many(
        string="Allowed To Finalization",
        comodel_name="res.groups",
        relation="rel_accountant_service_allowed_finalize_groups",
        column1="service_id",
        column2="group_id",
    )
    valid_grp_ids = fields.Many2many(
        string="Allowed To Validate",
        comodel_name="res.groups",
        relation="rel_accountant_service_allowed_valid_groups",
        column1="service_id",
        column2="group_id",
    )
    cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel",
        comodel_name="res.groups",
        relation="rel_accountant_service_allowed_cancel_groups",
        column1="service_id",
        column2="group_id",
    )
    restart_grp_ids = fields.Many2many(
        string="Allowed To Restart",
        comodel_name="res.groups",
        relation="rel_accountant_service_allowed_restart_groups",
        column1="service_id",
        column2="group_id",
    )

    @api.multi
    def _get_localdict(self, report):
        self.ensure_one()
        return {
            "env": self.env,
            "service": self,
            "report": report,
        }

    @api.multi
    def _compute_sequence(self, report):
        self.ensure_one()
        result = ""
        localdict = self._get_localdict(report)
        try:
            eval(self.sequence_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            raise UserError(_("Error in report sequence computation"))
        return result

    @api.multi
    def _get_sequence(self, signing_accountant):
        obj_signing = self.env["accountant.report_signing_partner"]

        result = False
        sequence_signing = False
        criteria = [
            ("service_id", "=", self.id),
            ("signing_accountant_id", "=", signing_accountant.id),
        ]
        signs = obj_signing.search(criteria, limit=1)
        if len(signs) > 0:
            sequence_signing = signs[0]._get_sequence()
        if sequence_signing:
            result = sequence_signing
        elif self.sequence_id:
            result = self.sequence_id
        return result

    @api.multi
    def _mapped_policy_field(self):
        pairs = {
            "accountant_report_confirm_grp_ids": "confirm_grp_ids",
            "accountant_report_finalize_grp_ids": "finalize_grp_ids",
            "accountant_report_valid_grp_ids": "valid_grp_ids",
            "accountant_report_cancel_grp_ids": "cancel_grp_ids",
            "accountant_report_restart_grp_ids": "restart_grp_ids",
        }
        return pairs

    @api.multi
    def _get_button_policy(self, policy_field, signing_accountant_id):
        self.ensure_one()
        button_group_ids = []
        obj_signing = self.env["accountant.report_signing_partner"]
        criteria = [
            ("service_id", "=", self.id),
            ("signing_accountant_id", "=", signing_accountant_id.id),
        ]
        signings = obj_signing.search(criteria, limit=1)

        if len(signings) == 0:
            return button_group_ids

        ttd = signings[0]

        policy_field = self._mapped_policy_field().get(policy_field, False)

        button_group_ids = ttd._get_button_policy(policy_field)

        button_group_ids += getattr(self, policy_field).ids

        return button_group_ids


class AccountantReportSigningPartner(models.Model):
    _name = "accountant.report_signing_partner"
    _description = "Accountant Report Signing Partner"

    service_id = fields.Many2one(
        string="Accountant Service",
        comodel_name="accountant.service",
        ondelete="cascade",
    )
    signing_accountant_id = fields.Many2one(
        string="Signing Partner",
        comodel_name="res.partner",
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm",
        comodel_name="res.groups",
        relation="rel_signing_partner_allowed_confirm_groups",
        column1="signing_id",
        column2="group_id",
    )
    finalize_grp_ids = fields.Many2many(
        string="Allowed To Finalization",
        comodel_name="res.groups",
        relation="rel_signing_partner_allowed_finalize_groups",
        column1="signing_id",
        column2="group_id",
    )
    valid_grp_ids = fields.Many2many(
        string="Allowed To Validate",
        comodel_name="res.groups",
        relation="rel_signing_partner_allowed_valid_groups",
        column1="signing_id",
        column2="group_id",
    )
    cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel",
        comodel_name="res.groups",
        relation="rel_signing_partner_allowed_cancel_groups",
        column1="signing_id",
        column2="group_id",
    )
    restart_grp_ids = fields.Many2many(
        string="Allowed To Restart",
        comodel_name="res.groups",
        relation="rel_signing_partner_allowed_restart_groups",
        column1="service_id",
        column2="group_id",
    )

    @api.multi
    def _get_sequence(self):
        result = False
        if self.sequence_id:
            result = self.sequence_id

        return result

    @api.multi
    def _get_button_policy(self, policy_field):
        self.ensure_one()
        button_group_ids = []

        button_group_ids += getattr(self, policy_field).ids

        return button_group_ids
