# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class AccountantReport(models.Model):
    _name = "accountant.report"
    _description = "Accountant Report"
    _inherit = [
        "mail.thread",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _order = "date desc, id"

    @api.model
    def _default_name(self):
        return "/"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    def _compute_policy(self):
        _super = super(AccountantReport, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "service_id",
    )
    def _compute_signing_partner(self):
        obj_signing = self.env["accountant.report_signing_partner"]
        for report in self:
            result = []
            criteria = [
                ("service_id", "=", report.service_id.id),
            ]
            for signing in obj_signing.search(criteria):
                result.append(signing.signing_accountant_id.id)
            report.allowed_signing_accountant_ids = [(6, 0, result)]

    @api.multi
    @api.depends(
        "service_id",
    )
    def _compute_opinion(self):
        for report in self:
            report.allowed_opinion_ids = [
                (6, 0, report.service_id.allowed_opinion_ids.ids)
            ]

    @api.multi
    @api.depends(
        "service_id",
    )
    def _compute_method(self):
        for report in self:
            report.allowed_method_ids = [
                (6, 0, report.service_id.allowed_method_ids.ids)
            ]

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
    signing_accountant_id = fields.Many2one(
        string="Signing Accountant",
        required=True,
        translate=False,
        comodel_name="res.partner",
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
    allowed_signing_accountant_ids = fields.Many2many(
        string="Allowed Signing Partner",
        comodel_name="res.partner",
        compute="_compute_signing_partner",
        store=False,
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
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    finalize_date = fields.Datetime(
        string="Finalization Date",
        readonly=True,
        copy=False,
    )
    finalize_user_id = fields.Many2one(
        string="Finalized By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    finalize_ok = fields.Boolean(
        string="Can Finalization",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    valid_date = fields.Datetime(
        string="Validation Date",
        readonly=True,
        copy=False,
    )
    valid_user_id = fields.Many2one(
        string="Validated By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    valid_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancelation Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Canceled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )

    @api.multi
    def action_confirm(self):
        for report in self:
            report.write(self._prepare_confirm_data())

    @api.multi
    def action_finalize(self):
        for report in self:
            report.write(self._prepare_finalize_data())

    @api.multi
    def action_valid(self):
        for report in self:
            report.write(self._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for report in self:
            report.write(self._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for report in self:
            report.write(self._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_finalize_data(self):
        self.ensure_one()
        result = {
            "name": self._create_sequence(),
            "state": "finalize",
            "finalize_date": fields.Datetime.now(),
            "finalize_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        result = {
            "state": "valid",
            "valid_date": fields.Datetime.now(),
            "valid_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "finalize_date": False,
            "finalize_user_id": False,
            "valid_date": False,
            "valid_user_id": False,
        }
        return result

    @api.multi
    def _prepare_create_data(self):
        return {}

    @api.multi
    def _get_sequence(self):
        self.ensure_one()
        company = self.env.user.company_id
        sequence_kategori = self.service_id._get_sequence(self.signing_accountant_id)

        if sequence_kategori:
            result = sequence_kategori
        elif company.accountant_report_sequence_id:
            result = company.accountant_report_sequence_id
        else:
            result = self.env.ref("accountant_report.sequence_accountant_report")
        return result

    @api.multi
    def _create_sequence(self):
        self.ensure_one()
        if self.service_id.sequence_creation_method == "standard" and self.name == "/":
            result = self.env["ir.sequence"].next_by_id(self._get_sequence().id) or "/"
        elif (
            self.service_id.sequence_creation_method != "standard" and self.name == "/"
        ):
            result = self.service_id._compute_sequence(self)
        else:
            result = self.name
        return result

    @api.model
    def create(self, values):
        report = super(AccountantReport, self).create(values)
        report.write(report._prepare_create_data())
        return report

    @api.multi
    def _get_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids = self.service_id._get_button_policy(
            policy_field, self.signing_accountant_id
        )

        button_group_ids += getattr(self.company_id, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if set(button_group_ids) & set(group_ids):
                result = True
        return result

    @api.onchange("service_id")
    def onchange_signing_accountant_id(self):
        self.signing_accountant_id = False

    @api.onchange("service_id")
    def onchange_report_opinion_id(self):
        self.report_opinion_id = False

    @api.onchange("service_id")
    def onchange_method_id(self):
        self.method_id = False

    @api.multi
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

    @api.multi
    def name_get(self):
        result = []
        for move in self:
            if move.name == "/":
                name = "*" + str(move.id)
            else:
                name = move.name
            result.append((move.id, name))
        return result
