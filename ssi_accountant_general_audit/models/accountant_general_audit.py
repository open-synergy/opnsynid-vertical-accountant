# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantGeneralAudit(models.Model):
    _name = "accountant.general_audit"
    _description = "Accountant General Audit"
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
        res = super(AccountantGeneralAudit, self)._get_policy_field()
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
        _super = super(AccountantGeneralAudit, self)
        _super._compute_policy()

    @api.depends(
        "trial_balance_ids",
    )
    def _compute_trial_balance_id(self):
        for document in self:
            document.trial_balance_id = False
            if len(document.trial_balance_ids) > 0:
                document.trial_balance_id = document.trial_balance_ids[0]

    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        copy=False,
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
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_type_set_id = fields.Many2one(
        string="Account Type Set",
        comodel_name="accountant.client_account_type_set",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    financial_accounting_standard_id = fields.Many2one(
        string="Financial Accounting Standard",
        comodel_name="accountant.financial_accounting_standard",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    opinion_id = fields.Many2one(
        string="Opinion",
        comodel_name="accountant.general_audit_opinion",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_firm = fields.Integer(
        string="Num. of Consecutive Audit (Firm)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_accountant = fields.Integer(
        string="Num. of Consecutive Audit (Accountant)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_option = fields.Selection(
        string="Restatement Option",
        selection=[
            ("no", "Not a restatement"),
            ("internal", "Restated audit exist in Odoo"),
            ("external", "Restated audit does not exist in Odoo"),
        ],
        required=True,
        default="no",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit_id = fields.Many2one(
        string="Previous # Audit",
        comodel_name="accountant.general_audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit = fields.Char(
        string="Previous Audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    worksheet_ids = fields.One2many(
        string="Worksheets",
        comodel_name="accountant.general_audit_worksheet",
        inverse_name="general_audit_id",
        readonly=True,
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
    trial_balance_ids = fields.Many2many(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        relation="rel_general_audit_2_trial_balance",
        column1="general_audit_id",
        column2="trial_balance_id",
    )
    trial_balance_id = fields.Many2one(
        string="# Trial Balance",
        comodel_name="accountant.client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )

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
                    "Interim Date end must be greater than Interim Date start"
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
                    "Interim Date start must be greater than previous Interim Date end"
                )
                if record.previous_date_end >= record.interim_date_start:
                    raise UserError(strWarning)
