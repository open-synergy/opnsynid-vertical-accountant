# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantReportMixin(models.AbstractModel):
    _name = "accountant.report_mixin"
    _description = "Accountant Report Mixin"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.date_duration",
    ]
    _order = "date desc, id"

    # Attribute related to multiple approval
    _approval_from_state = "ready"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attribute related to sequence
    _create_sequence_state = "ready"

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,ready,confirm,done"
    _policy_field_order = [
        "ready_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_ready",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_ready",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    @api.model
    def _get_policy_field(self):
        res = super(AccountantReportMixin, self)._get_policy_field()
        policy_field = [
            "done_ok",
            "confirm_ok",
            "approve_ok",
            "ready_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    partner_id = fields.Many2one(
        string="Customer",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="res.partner",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    primary_sector_id = fields.Many2one(
        string="Primary Sector",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="res.partner.industry",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    primary_creditor_id = fields.Many2one(
        string="Primary Creditor",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="res.partner",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    signing_accountant_id = fields.Many2one(
        string="Signing Accountant",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="res.partner",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    service_id = fields.Many2one(
        string="Accountant Service",
        required=True,
        translate=False,
        readonly=True,
        comodel_name="accountant.service",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        translate=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    firm_subsequent_num = fields.Integer(
        string="Firm Subsequent Job Num.",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    accountant_subsequent_num = fields.Integer(
        string="Accountant Subsequent Job Num.",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement = fields.Boolean(
        string="Restatement?",
        default=False,
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
            ("manual", "Manual"),
            ("odoo", "Odoo"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_number = fields.Char(
        string="# Restatement (Manual)",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_id = fields.Many2one(
        string="# Restatement",
        comodel_name="accountant.report_mixin",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        required=True,
        translate=False,
        readonly=True,
        selection=[
            ("draft", "Draft"),
            ("ready", "Ready To Process"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )

    @api.onchange("restatement")
    def onchange_restatement_option(self):
        self.restatement_option = False
