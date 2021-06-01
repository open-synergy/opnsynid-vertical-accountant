# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PartnerArrangement(models.Model):
    _name = "accountant.partner_arrangement"
    _description = "Partner Arrangement"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _order = "date desc"
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]

    @api.model
    def _default_name(self):
        return "/"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    name = fields.Char(
        string="# Partner Arrangement",
        required=True,
        translate=False,
        default=lambda self: self._default_name(),
        readonly=True,
        copy=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        translate=False,
        default=lambda self: self._default_company_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    managing_partner_id = fields.Many2one(
        string="Managing Partner",
        required=True,
        translate=False,
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_ids = fields.Many2many(
        string="Partners",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Arrangement Date",
        required=True,
        translate=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        required=True,
        translate=False,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("valid", "Valid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    valid_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    valid_date = fields.Datetime(
        string="Validation Date",
        readonly=True,
        copy=False,
    )
    valid_user_id = fields.Many2one(
        string="Valid By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    @api.multi
    def action_confirm(self):
        for arrangement in self:
            arrangement.write(arrangement._prepare_confirm_data())
            arrangement.request_validation()

    @api.multi
    def action_valid(self):
        for arrangement in self:
            arrangement.write(arrangement._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for arrangement in self:
            arrangement.write(arrangement._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for arrangement in self:
            arrangement.write(self._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        # "name": sequence,
        result = {
            "state": "valid",
            "valid_date": fields.Datetime.now(),
            "valid_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "valid_date": False,
            "valid_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }
        return result

    @api.model
    def _prepare_create_data(self, values):
        name = values.get("name", False)
        company_id = values.get("company_id", False)
        if not name or name == "/":
            values["name"] = self._create_sequence(company_id)
        return values

    @api.model
    def _get_sequence(self, company_id):
        company = self.env["res.company"].browse([company_id])[0]

        if company.accountant_partner_arrangement_sequence_id:
            result = company.accountant_partner_arrangement_sequence_id
        else:
            result = self.env.ref(
                "accountant_partner_arrangement.sequence_accountant_"
                "partner_arrangement"
            )
        return result

    @api.model
    def _create_sequence(self, company_id):
        name = (
            self.env["ir.sequence"].next_by_id(self._get_sequence(company_id).id) or "/"
        )
        return name

    @api.model
    def create(self, values):
        new_values = self._prepare_create_data(values)
        return super(PartnerArrangement, self).create(new_values)

    @api.multi
    def unlink(self):
        _super = super(PartnerArrangement, self)
        force_unlink = self._context.get("force_unlink", False)
        for report in self:
            if report.state != "draft" and not force_unlink:
                raise UserError(_("You can only delete data with draft state"))
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(PartnerArrangement, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(PartnerArrangement, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    @api.onchange("company_id")
    def onchange_managing_partner_id(self):
        value = {
            "managing_partner_id": False,
        }
        domain = {
            "managing_partner_id": [("id", "=", 0)],
        }
        if self.company_id:
            partner = self.company_id.partner_id
            domain["managing_partner_id"] = [
                ("commercial_partner_id.id", "=", partner.id),
                ("is_company", "=", False),
            ]
        return {"value": value, "domain": domain}

    @api.onchange("company_id")
    def onchange_partner_ids(self):
        value = {
            "partner_ids": [(6, 0, [])],
        }
        domain = {
            "partner_ids": [("id", "=", 0)],
        }
        if self.company_id:
            partner = self.company_id.partner_id
            domain["partner_ids"] = [
                ("commercial_partner_id.id", "=", partner.id),
                ("is_company", "=", False),
            ]
        return {"value": value, "domain": domain}
