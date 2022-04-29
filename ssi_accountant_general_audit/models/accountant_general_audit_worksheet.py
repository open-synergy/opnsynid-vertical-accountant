# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantGeneralAuditWorksheet(models.Model):
    _name = "accountant.general_audit_worksheet"
    _description = "Accountant General Audit Worksheet"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
    ]
    _order = "general_audit_id, parent_type_id, id"

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = False

    _done_state = "valid"

    @api.model
    def _get_policy_field(self):
        res = super(AccountantGeneralAuditWorksheet, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
        ]
        res += policy_field
        return res

    def _compute_policy(self):
        _super = super(AccountantGeneralAuditWorksheet, self)
        _super._compute_policy()

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.general_audit_worksheet_type",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="accountant.general_audit_worksheet_conclusion",
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
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
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    # Policy Field
    done_ok = fields.Boolean(
        string="Can Valid",
    )
