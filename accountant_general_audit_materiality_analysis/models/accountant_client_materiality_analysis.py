# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountantClientMaterialityAnalysis(models.Model):
    _name = "accountant.client_materiality_analysis"
    _description = "Accountant Client Materiality Analysis"
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
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(AccountantClientMaterialityAnalysis, self)
        _super._compute_policy()

    name = fields.Char(
        string="Document #",
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
    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        related="trial_balance_id.company_id",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        related="trial_balance_id.partner_id",
    )
    date_start = fields.Date(
        string="Start Date",
        readonly=True,
        related="trial_balance_id.date_start",
    )
    date_end = fields.Date(
        string="End Date",
        readonly=True,
        related="trial_balance_id.date_end",
    )
    balance_date_start = fields.Date(
        string="Balance Start Date",
        readonly=True,
        related="trial_balance_id.balance_date_start",
    )
    balance_date_end = fields.Date(
        string="Balance End Date",
        readonly=True,
        related="trial_balance_id.balance_date_end",
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        readonly=True,
        related="trial_balance_id.previous_date_start",
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        readonly=True,
        related="trial_balance_id.previous_date_end",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        related="trial_balance_id.currency_id",
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        readonly=True,
        related="trial_balance_id.account_type_set_id",
    )
    materiality_computation_item_id = fields.Many2one(
        string="Materiality Computation Item",
        comodel_name="accountant.trial_balance_computation_item",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    overall_materiality_percentage = fields.Float(
        string="Overall Materiality Percentage",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "materiality_computation_item_id",
        "overall_materiality_percentage",
    )
    def _compute_overall_materiality(self):
        result = 0.0
        for document in self:
            base = 100.0
            result = (base * document.overall_materiality_percentage) / 100.00
            document.overall_materiality = result

    overall_materiality = fields.Float(
        string="Overall Materiality",
        compute="_compute_overall_materiality",
        store=True,
    )
    performance_materiality_percentage = fields.Float(
        string="Performance Materiality Percentage",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "materiality_computation_item_id",
        "performance_materiality_percentage",
    )
    def _compute_performance_materiality(self):
        result = 0.0
        for document in self:
            base = 100.0
            result = (base * document.performance_materiality_percentage) / 100.00
            document.performance_materiality = result

    performance_materiality = fields.Float(
        string="Performance Materiality",
        compute="_compute_performance_materiality",
        store=True,
    )
    materiality_type = fields.Selection(
        string="Materiality Type",
        selection=[
            ("om", "Overall Materiality"),
            ("pm", "Performance Materiality"),
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
        string="Detail",
        comodel_name="accountant.client_materiality_analysis_detail",
        inverse_name="materiality_analysis_id",
        copy=True,
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
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
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
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountantClientMaterialityAnalysis, self)
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
        _super = super(AccountantClientMaterialityAnalysis, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantClientMaterialityAnalysis, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()
