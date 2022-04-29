# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantGeneralAuditWorksheetMixin(models.AbstractModel):
    _name = "accountant.general_audit_worksheet_mixin"
    _description = "Accountant General Audit Worksheet Mixin"
    _inherits = {
        "accountant.general_audit_worksheet": "worksheet_id",
    }
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]
    _type_xml_id = False

    @api.multi
    def _compute_type_id(self):
        for record in self:
            if self.worksheet_id:
                worksheet = self.worksheet_id
                record.type_id = worksheet.type_id

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="accountant.general_audit_worksheet",
        readonly=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.general_audit_worksheet_type",
        default=lambda self: self._default_type_id(),
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_conclusion_ids = fields.Many2many(
        string="Allowed Conculsion",
        comodel_name="accountant.general_audit_worksheet_conclusion",
        compute="_compute_allowed_conclusion_ids",
        store=False,
    )
    # Fields related from general audit
    date_start = fields.Date(
        string="Start Date",
        readonly=True,
    )
    date_end = fields.Date(
        string="End Date",
        readonly=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        readonly=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        readonly=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        readonly=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        readonly=True,
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        readonly=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="general_audit_id.partner_id",
    )

    # policy fields
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    # log fields
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

    @api.model
    def _default_type_id(self):
        result = False
        if self._type_xml_id:
            result = self.env.ref(self._type_xml_id)
        return result

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_policy(self):
        _super = super(AccountantGeneralAuditWorksheetMixin, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_allowed_conclusion_ids(self):
        obj_conslusion = self.env["accountant.general_audit_worksheet_conclusion"]
        for record in self:
            result = []
            if record.type_id:
                criteria = [
                    ("type_id", "=", record.type_id.id),
                ]
                result = obj_conslusion.search(criteria).ids
            record.allowed_conclusion_ids = result

    @api.onchange("type_id")
    def onchange_parent_type_id(self):
        self.parent_type_id = self.type_id

    @api.onchange("type_id")
    def onchange_conclusion_id(self):
        self.conslusion_id = False

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_valid(self):
        for record in self:
            record.write(record._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "valid",
            "name": sequence,
            "valid_date": fields.Datetime.now(),
            "valid_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "valid_date": False,
            "valid_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        worksheets = self.env["accountant.general_audit_worksheet"]
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
            worksheets += record.worksheet_id
        _super = super(AccountantGeneralAuditWorksheetMixin, self)
        _super.unlink()
        worksheets.unlink()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.multi
    def validate_tier(self):
        _super = super(AccountantGeneralAuditWorksheetMixin, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantGeneralAuditWorksheetMixin, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()
