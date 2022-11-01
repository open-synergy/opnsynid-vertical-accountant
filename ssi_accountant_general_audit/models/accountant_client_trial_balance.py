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

    # Attributes related to multiple approval
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "open"

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
            "manual_number_ok",
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

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    trial_balance_type = fields.Selection(
        string="Trial Balance Type",
        required=True,
        selection=[
            ("home", "Home Statement"),
            ("interim", "Interim"),
            ("previous", "Previous"),
        ],
        default="home",
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
            "open": [
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

    def action_reload_account(self):
        for record in self.sudo():
            record._reload_account()

    def action_recompute_computation(self):
        for record in self.sudo():
            record._recompute_computation()

    def _reload_account(self):
        self.ensure_one()
        ClientAccount = self.env["accountant.client_account"]
        Detail = self.env["accountant.client_trial_balance_detail"]
        criteria = [
            ("partner_id", "=", self.partner_id.id),
        ]
        for account in ClientAccount.search(criteria):
            details = self.detail_ids.filtered(lambda r: r.account_id.id == account.id)
            if len(details) == 0:
                Detail.create(
                    {
                        "account_id": account.id,
                        "trial_balance_id": self.id,
                    }
                )

    def _recompute_computation(self):
        self.ensure_one()
        for computation in self.computation_ids:
            computation.action_recompute()
