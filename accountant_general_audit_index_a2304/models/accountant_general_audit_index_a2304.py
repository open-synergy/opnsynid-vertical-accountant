# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountantGeneralAuditIndexA2304(models.Model):
    _name = "accountant.general_audit_index_a2304"
    _description = "Accountant General Audit Index A.230.4"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["valid"]

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(AccountantGeneralAuditIndexA2304, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "general_audit_ids",
    )
    def _compute_general_audit_id(self):
        for document in self:
            document.general_audit_id = False
            if len(document.general_audit_ids) > 0:
                document.general_audit_id = document.general_audit_ids[0]

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _inverse_general_audit(self):
        for document in self:
            if not document.general_audit_id:
                continue
            document.general_audit_ids = [(6, 0, [document.general_audit_id.id])]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        store=True,
        compute="_compute_general_audit_id",
        inverse="_inverse_general_audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    general_audit_ids = fields.Many2many(
        string="General Audits",
        comodel_name="accountant.general_audit",
        relation="rel_general_audit_2_index_a2304",
        column1="index_a2304_id",
        column2="general_audit_id",
    )
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        readonly=True,
        related="general_audit_id.company_id",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        readonly=True,
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        store=True,
        related="general_audit_id.currency_id",
    )
    relevant_regulation_ids = fields.One2many(
        string="Relevant Regulation",
        comodel_name="accountant.general_audit_relevant_regulation",
        inverse_name="index_a2304_id",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        # copy=True,
    )
    status_id = fields.Many2one(
        string="Status",
        comodel_name="accountant.general_audit_index_a2304_status",
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("valid", "Valid"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )
    valid_ok = fields.Boolean(
        string="Can Valid",
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
    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountantGeneralAuditIndexA2304, self)
        _super.unlink()

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
        _super = super(AccountantGeneralAuditIndexA2304, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantGeneralAuditIndexA2304, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()
