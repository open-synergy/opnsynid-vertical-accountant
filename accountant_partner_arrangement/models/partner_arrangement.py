# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, SUPERUSER_ID
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PartnerArrangement(models.Model):
    _name = "accountant.partner_arrangement"
    _description = "Partner Arrangement"
    _inherit = "mail.thread"
    _order = "date desc"

    @api.model
    def _default_name(self):
        return "/"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    @api.depends(
        "state",
        "company_id",
    )
    def _compute_policy(self):
        for arrangement in self:
            if self.env.user.id == SUPERUSER_ID:
                arrangement.confirm_ok = arrangement.valid_ok = \
                    arrangement.cancel_ok = \
                    arrangement.restart_ok = True
                continue

            if arrangement.company_id:
                company = arrangement.company_id
                for policy in company.\
                        _get_partner_arrangement_button_policy_map():
                    setattr(
                        arrangement,
                        policy[0],
                        company.
                        _get_partner_arrangement_button_policy(
                            policy[1]),
                    )

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

    @api.multi
    def action_confirm(self):
        for arrangement in self:
            arrangement.write(self._prepare_confirm_data())

    @api.multi
    def action_valid(self):
        for arrangement in self:
            arrangement.write(self._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for arrangement in self:
            arrangement.write(self._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for arrangement in self:
            arrangement.write(self._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
        }
        return result

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        result = {
            "state": "valid",
        }
        return result

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
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
                "partner_arrangement")
        return result

    @api.model
    def _create_sequence(self, company_id):
        name = self.env["ir.sequence"].\
            next_by_id(self._get_sequence(company_id).id) or "/"
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
