# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantReport(models.Model):
    _name = "accountant.report"
    _description = "Accountant Report"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _order = "date desc, id"
    _approval_from_state = "draft"
    _approval_to_state = "valid"
    _approval_state = "confirm"
    _after_approved_method = "action_open"
    _create_sequence_state = "valid"
    _open_state = "valid"
    _done_state = "finalize"

    @api.depends(
        "service_id",
    )
    def _compute_opinion(self):
        for report in self:
            report.allowed_opinion_ids = [
                (6, 0, report.service_id.allowed_opinion_ids.ids)
            ]

    @api.depends(
        "service_id",
    )
    def _compute_method(self):
        for report in self:
            report.allowed_method_ids = [
                (6, 0, report.service_id.allowed_method_ids.ids)
            ]

    @api.model
    def _get_policy_field(self):
        res = super(AccountantReport, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    name = fields.Char(
        string="# Report",
    )
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
    opinion_required = fields.Boolean(
        string="Opinion Required",
        related="service_id.opinion_required",
        readonly=True,
    )
    method_required = fields.Boolean(
        string="Method Required",
        related="service_id.method_required",
        readonly=True,
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
    date_start = fields.Date(
        string="Date Start",
        required=True,
        translate=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    subsequent_num = fields.Integer(
        string="Subsequent Job Num.",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_id = fields.Many2one(
        string="Restatement Report",
        comodel_name="accountant.report",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        translate=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    assurance = fields.Boolean(
        string="Assurance",
    )
    opinion_id = fields.Many2one(
        string="Opinion",
        required=False,
        translate=False,
        readonly=True,
        comodel_name="accountant.report_opinion",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    method_id = fields.Many2one(
        string="Method",
        required=False,
        translate=False,
        readonly=True,
        comodel_name="accountant.report_method",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_opinion_ids = fields.Many2many(
        string="Allowed Opinion",
        comodel_name="accountant.report_opinion",
        compute="_compute_opinion",
        store=False,
    )
    allowed_method_ids = fields.Many2many(
        string="Allowed Methods",
        comodel_name="accountant.report_method",
        compute="_compute_method",
        store=False,
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
            ("finalize", "Finalization"),
            ("reject", "Rejected"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )

    def _compute_policy(self):
        _super = super(AccountantReport, self)
        _super._compute_policy()

    # Policy Field
    done_ok = fields.Boolean(
        string="Can Finalization",
    )
    open_ok = fields.Boolean(
        string="Can Validate",
    )

    @api.onchange("service_id")
    def onchange_report_opinion_id(self):
        self.opinion_id = False
        if self.service_id:
            self.opinion_id = self.service_id.allowed_opinion_ids

    @api.onchange("service_id")
    def onchange_method_id(self):
        self.method_id = False
        if self.service_id:
            self.method_id = self.service_id.allowed_method_ids
