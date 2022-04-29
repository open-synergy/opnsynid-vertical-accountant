# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantClientTrialBalance(models.Model):
    _name = "accountant.client_trial_balance"
    _description = "Accountant Client Trial Balance"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
        "mixin.transaction_done",
    ]

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "done"

    @api.model
    def _get_policy_field(self):
        res = super(AccountantClientTrialBalance, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(AccountantClientTrialBalance, self)
        _super._compute_policy()

    @api.depends(
        "general_audit_id",
    )
    def _inverse_general_audit(self):
        for document in self:
            if not document.general_audit_id:
                continue
            document.general_audit_ids = [(6, 0, [document.general_audit_id.id])]

    @api.depends(
        "general_audit_ids",
    )
    def _compute_general_audit_id(self):
        for document in self:
            document.general_audit_id = False
            if len(document.general_audit_ids) > 0:
                document.general_audit_id = document.general_audit_ids[0]

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
        relation="rel_general_audit_2_trial_balance",
        column1="trial_balance_id",
        column2="general_audit_id",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        store=True,
        readonly=True,
    )
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        store=True,
        readonly=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        store=True,
        readonly=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        store=True,
        readonly=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        store=True,
        readonly=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        store=True,
        readonly=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=True,
        readonly=True,
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        related="general_audit_id.account_type_set_id",
        store=True,
        readonly=True,
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "account_type_set_id",
    )
    def _compute_account_type_ids(self):
        for document in self:
            result = []
            if document.account_type_set_id:
                type_set = document.account_type_set_id
                result = type_set.detail_ids
        document.allowed_type_ids = result

    allowed_type_ids = fields.Many2many(
        string="Allowed Account Type",
        comodel_name="accountant.client_account_type",
        compute="_compute_account_type_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="accountant.client_trial_balance_detail",
        inverse_name="trial_balance_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    standard_detail_ids = fields.One2many(
        string="Standard Detail",
        comodel_name="accountant.client_trial_balance_standard_detail",
        inverse_name="trial_balance_id",
        readonly=True,
        copy=True,
    )
    computation_ids = fields.One2many(
        string="Computation",
        comodel_name="accountant.client_trial_balance_computation",
        inverse_name="trial_balance_id",
        readonly=True,
        copy=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "On Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    def action_recompute(self):
        for record in self:
            record.computation_ids.action_recompute()

    @api.onchange("account_type_set_id")
    def onchange_standard_detail_ids(self):
        self.update({"standard_detail_ids": [(5, 0, 0)]})
        if self.account_type_set_id:
            result = []
            for detail in self.account_type_set_id.detail_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "sequence": detail.sequence,
                            "type_id": detail.id,
                        },
                    )
                )
            self.update({"standard_detail_ids": result})

    @api.onchange("account_type_set_id")
    def onchange_computation_ids(self):
        self.update({"computation_ids": [(5, 0, 0)]})
        if self.account_type_set_id:
            result = []
            for detail in self.account_type_set_id.computation_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "computation_item_id": detail.computation_id.id,
                        },
                    )
                )
            self.update({"computation_ids": result})

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    @api.constrains("interim_date_start", "interim_date_end")
    def _check_interim_date_start_end(self):
        for record in self:
            if record.interim_date_start and record.interim_date_end:
                strWarning = _(
                    "Balance Date end must be greater than Balance date start"
                )
                if record.interim_date_end < record.interim_date_start:
                    raise UserError(strWarning)

    @api.constrains("previous_date_start", "previous_date_end")
    def _check_previous_date_start_end(self):
        for record in self:
            if record.previous_date_start and record.previous_date_end:
                strWarning = _(
                    "Previous Date end must be greater than Previous date start"
                )
                if record.previous_date_end < record.previous_date_start:
                    raise UserError(strWarning)

    @api.constrains("interim_date_start", "previous_date_end")
    def _check_previous_interim_date(self):
        for record in self:
            if record.interim_date_start and record.previous_date_end:
                strWarning = _(
                    "Balance date start must be greater than previous balance date end"
                )
                if record.previous_date_end >= record.interim_date_start:
                    raise UserError(strWarning)
