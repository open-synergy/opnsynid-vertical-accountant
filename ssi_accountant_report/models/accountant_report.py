# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class AccountantReport(models.Model):
    _name = "accountant.report"
    _description = "Accountant Report"
    _inherit = [
        "mixin.policy",
        "mixin.sequence",
        "mail.thread",
    ]
    _order = "date desc, id"

    @api.model
    def _default_name(self):
        return "/"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

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
            "finalize_ok",
            "valid_ok",
            "cancel_ok",
            "restart_ok",
        ]
        res += policy_field
        return res

    name = fields.Char(
        string="# Report",
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
    information_based = fields.Selection(
        string="Information Based On",
        selection=[
            ("yearly", "Yearly Financial Report"),
            ("interim", "Interim Financial Report"),
        ],
        default="yearly",
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
    report_currency_id = fields.Many2one(
        string="Client Currency",
        comodel_name="res.currency",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    revenue = fields.Float(
        string="Revenue",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    ebit = fields.Float(
        string="EBIT",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_expense = fields.Float(
        string="Tax Expense",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    total_asset = fields.Float(
        string="Total Asset",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    total_liability = fields.Float(
        string="Total Liability",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    total_net_profit = fields.Float(
        string="Total Net Profit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    total_net_profit_oci = fields.Float(
        string="Total Net Profit & OCI",
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
    report_opinion_id = fields.Many2one(
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
    note = fields.Text(
        string="Note",
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
            ("finalize", "Finalization"),
            ("valid", "Valid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )

    def _compute_policy(self):
        _super = super(AccountantReport, self)
        _super._compute_policy()

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        readonly=True,
    )
    finalize_ok = fields.Boolean(
        string="Can Finalization",
        compute="_compute_policy",
        readonly=True,
    )
    valid_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        readonly=True,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        readonly=True,
    )

    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
        }
        return result

    def action_confirm(self):
        for report in self:
            report.write(self._prepare_confirm_data())

    def _prepare_finalize_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        result = {
            "name": sequence,
            "state": "finalize",
        }
        return result

    def action_finalize(self):
        for report in self:
            report.write(self._prepare_finalize_data())

    def _prepare_valid_data(self):
        self.ensure_one()
        result = {
            "state": "valid",
        }
        return result

    def action_valid(self):
        for report in self:
            report.write(self._prepare_valid_data())

    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
        }
        return result

    def action_cancel(self):
        for report in self:
            report.write(self._prepare_cancel_data())

    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
        }
        return result

    def action_restart(self):
        for report in self:
            report.write(self._prepare_restart_data())

    def _prepare_create_data(self):
        return {}

    @api.model
    def create(self, values):
        report = super(AccountantReport, self).create(values)
        report.write(report._prepare_create_data())
        return report

    @api.onchange("service_id")
    def onchange_report_opinion_id(self):
        self.report_opinion_id = False
        if self.service_id:
            self.report_opinion_id = self.service_id.allowed_opinion_ids

    @api.onchange("service_id")
    def onchange_method_id(self):
        self.method_id = False
        if self.service_id:
            self.method_id = self.service_id.allowed_method_ids

    def unlink(self):
        _super = super(AccountantReport, self)
        force_unlink = self._context.get("force_unlink", False)
        for report in self:
            if report.state != "draft" or report.name != "/" and not force_unlink:
                msg_warning = _(
                    "You can only delete data with draft state "
                    "and name is equal to '/'"
                )
                raise UserError(msg_warning)
        _super.unlink()

    def name_get(self):
        result = []
        for move in self:
            if move.name == "/":
                name = "*" + str(move.id)
            else:
                name = move.name
            result.append((move.id, name))
        return result
