# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantClientAdjustmentEntry(models.Model):
    _name = "accountant.client_adjustment_entry"
    _description = "Accountant Client Adjustment Entry"
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
        res = super(AccountantClientAdjustmentEntry, self)._get_policy_field()
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

    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(AccountantClientAdjustmentEntry, self)
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
    adjustment_type = fields.Selection(
        string="Adjustment Type",
        selection=[
            ("propose", "Proposed Adjustment"),
            ("client", "Client Adjustment"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="accountant.client_adjustment_entry_detail",
        inverse_name="entry_id",
        readonly=True,
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

    @api.constrains(
        "state",
    )
    def constrains_credit_debit(self):
        for record in self:
            if record.state not in ["draft", "cancel"]:
                total_debit = 0.0
                total_credit = 0.0
                for line in self.detail_ids:
                    total_debit = total_debit + line.debit
                    total_credit = total_credit + line.credit
                if total_debit != total_credit:
                    msg = _("Total Credit and Total Debit must balance")
                    raise UserError(msg)
