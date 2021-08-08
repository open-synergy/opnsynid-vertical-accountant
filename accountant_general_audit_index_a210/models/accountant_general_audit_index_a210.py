# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval as eval


class AccountantGeneralAuditIndexA210(models.Model):
    _name = "accountant.general_audit_index_a210"
    _description = "Accountant General Audit Index A.210"
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
        "company_id",
    )
    def _compute_policy(self):
        _super = super(AccountantGeneralAuditIndexA210, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "general_audit_ids",
    )
    def _compute_general_audit_id(self):
        for document in self:
            document.general_audit_id = False
            if len(document.general_audit_ids) > 0:
                document.general_audit_id = document.general_audit_ids[0]

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _inverse_general_audit(self):
        for document in self:
            if not document.general_audit_id:
                continue
            document.general_audit_ids = [(6, 0, [document.general_audit_id.id])]

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_total_asset(self):
        for document in self:
            total_asset = total_asset_extrapolation = 0.0
            if document.general_audit_id:
                acc_type = document.general_audit_id.account_type_set_id
                try:
                    python_code = acc_type.total_asset_python_code
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    total_asset = localdict["result"]
                    total_asset_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    total_asset = total_asset_extrapolation = 0.0
            self.total_asset = total_asset
            self.total_asset_extrapolation = total_asset_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_net_asset(self):
        for document in self:
            net_asset = net_asset_extrapolation = 0.0
            if document.general_audit_id:
                acc_type = document.general_audit_id.account_type_set_id
                try:
                    python_code = acc_type.net_asset_python_code
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    net_asset = localdict["result"]
                    net_asset_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    net_asset = net_asset_extrapolation = 0.0
            self.net_asset = net_asset
            self.net_asset_extrapolation = net_asset_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_revenue(self):
        for document in self:
            revenue = revenue_extrapolation = 0.0
            if document.general_audit_id:
                acc_type = document.general_audit_id.account_type_set_id
                try:
                    python_code = acc_type.revenue_python_code
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    revenue = localdict["result"]
                    revenue_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    revenue = revenue_extrapolation = 0.0
            self.revenue = revenue
            self.revenue_extrapolation = revenue_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_cost_of_revenue(self):
        for document in self:
            cost_of_revenue = cost_of_revenue_extrapolation = 0.0
            if document.general_audit_id:
                acc_type = document.general_audit_id.account_type_set_id
                try:
                    python_code = acc_type.cost_of_revenue_python_code
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    cost_of_revenue = localdict["result"]
                    cost_of_revenue_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    cost_of_revenue = cost_of_revenue_extrapolation = 0.0
            self.cost_of_revenue = cost_of_revenue
            self.cost_of_revenue_extrapolation = cost_of_revenue_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_ebt(self):
        for document in self:
            ebt = ebt_extrapolation = 0.0
            if document.general_audit_id:
                try:
                    python_code = (
                        document.general_audit_id.account_type_set_id.ebt_python_code
                    )
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    ebt = localdict["result"]
                    ebt_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    ebt = ebt_extrapolation = 0.0
            self.ebt = ebt
            self.ebt_extrapolation = ebt_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_ebitda(self):
        for document in self:
            ebitda = ebitda_extrapolation = 0.0
            if document.general_audit_id:
                try:
                    python_code = (
                        document.general_audit_id.account_type_set_id.ebitda_python_code
                    )
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    ebitda = localdict["result"]
                    ebitda_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    ebitda = ebitda_extrapolation = 0.0
            self.ebitda = ebitda
            self.ebitda_extrapolation = ebitda_extrapolation

    @api.multi
    @api.depends(
        "general_audit_id",
    )
    def _compute_total_liability(self):
        for document in self:
            total_liability = total_liability_extrapolation = 0.0
            if document.general_audit_id:
                acc_type = document.general_audit_id.account_type_set_id
                try:
                    python_code = acc_type.total_liability_python_code
                    localdict = document._get_localdict()
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    total_liability = localdict["result"]
                    total_liability_extrapolation = localdict["result_extrapolation"]
                except Exception:
                    total_liability = total_liability_extrapolation = 0.0
            self.total_liability = total_liability
            self.total_liability_extrapolation = total_liability_extrapolation

    @api.multi
    @api.depends(
        "total_asset",
        "total_asset_extrapolation",
        "net_asset",
        "net_asset_extrapolation",
        "revenue",
        "revenue_extrapolation",
        "cost_of_revenue",
        "cost_of_revenue_extrapolation",
        "ebt",
        "ebt_extrapolation",
        "ebitda",
        "ebitda_extrapolation",
        "total_liability",
        "total_liability_extrapolation",
        "other_base_amount",
        "base_amount",
        "performance_materiality_percentage",
        "overall_materiality_percentage",
    )
    def _compute_materiality(self):
        for document in self:
            base_amount = base_amount_extrapolation = 0.0
            if document.base_amount == "total_asset":
                base_amount = document.total_asset
                base_amount_extrapolation = document.total_asset_extrapolation
            elif document.base_amount == "net_asset":
                base_amount = document.net_asset
                base_amount_extrapolation = document.net_asset_extrapolation
            elif document.base_amount == "revenue":
                base_amount = document.revenue
                base_amount_extrapolation = document.revenue_extrapolation
            elif document.base_amount == "cost_of_revenue":
                base_amount = document.cost_of_revenue
                base_amount_extrapolation = document.cost_of_revenue_extrapolation
            elif document.base_amount == "ebt":
                base_amount = document.ebt
                base_amount_extrapolation = document.ebt_extrapolation
            elif document.base_amount == "ebitda":
                base_amount = document.ebitda
                base_amount_extrapolation = document.ebitda_extrapolation
            elif document.base_amount == "total_liability":
                base_amount = document.total_liability
                base_amount_extrapolation = document.total_liability_extrapolation
            elif document.base_amount == "other_base_amount":
                base_amount = document.other_base_amount
                base_amount_extrapolation = document.other_base_amount
            document.overall_materiality = (
                document.overall_materiality_percentage / 100.00
            ) * base_amount
            document.overall_materiality_extrapolation = (
                document.overall_materiality_percentage / 100.00
            ) * base_amount_extrapolation
            document.performance_materiality = (
                document.performance_materiality_percentage / 100.00
            ) * document.overall_materiality
            document.performance_materiality_extrapolation = (
                document.performance_materiality_percentage / 100.00
            ) * document.overall_materiality_extrapolation
            document.tolerable_misstatement = (
                document.tolerable_misstatement_percentage / 100.00
            ) * document.performance_materiality
            document.tolerable_misstatement_extrapolation = (
                document.tolerable_misstatement_percentage / 100.00
            ) * document.performance_materiality_extrapolation

    name = fields.Char(
        string="# Document",
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
        relation="rel_general_audit_2_index_a210",
        column1="index_a210_id",
        column2="general_audit_id",
    )
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
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
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="accountant.client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        readonly=True,
        related="general_audit_id.company_id",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="general_audit_id.partner_id",
        readonly=True,
        store=True,
    )
    total_asset = fields.Float(
        string="Total Asset",
        required=False,
        readonly=True,
        compute="_compute_total_asset",
        store=True,
    )
    total_asset_extrapolation = fields.Float(
        string="Extrapolation Total Asset",
        required=False,
        readonly=True,
        compute="_compute_total_asset",
        store=True,
    )
    net_asset = fields.Float(
        string="Net Asset",
        required=False,
        readonly=True,
        compute="_compute_net_asset",
        store=True,
    )
    net_asset_extrapolation = fields.Float(
        string="Extrapolation Net Asset",
        required=False,
        readonly=True,
        compute="_compute_net_asset",
        store=True,
    )
    revenue = fields.Float(
        string="Revenue",
        required=False,
        readonly=True,
        compute="_compute_revenue",
        store=True,
    )
    revenue_extrapolation = fields.Float(
        string="Extrapolation Revenue",
        required=False,
        readonly=True,
        compute="_compute_revenue",
        store=True,
    )
    cost_of_revenue = fields.Float(
        string="Cost of Revenue",
        required=False,
        readonly=True,
        compute="_compute_cost_of_revenue",
        store=True,
    )
    cost_of_revenue_extrapolation = fields.Float(
        string="Extrapolation Cost of Revenue",
        required=False,
        readonly=True,
        compute="_compute_cost_of_revenue",
        store=True,
    )
    ebt = fields.Float(
        string="EBT",
        required=False,
        readonly=True,
        compute="_compute_ebt",
        store=True,
    )
    ebt_extrapolation = fields.Float(
        string="Extrapolation EBT",
        required=False,
        readonly=True,
        compute="_compute_ebt",
        store=True,
    )
    ebitda = fields.Float(
        string="EBITDA",
        required=False,
        readonly=True,
        compute="_compute_ebitda",
        store=True,
    )
    ebitda_extrapolation = fields.Float(
        string="Extrapolation EBITDA",
        required=False,
        readonly=True,
        compute="_compute_ebitda",
        store=True,
    )
    total_liability = fields.Float(
        string="Total Liability",
        required=False,
        readonly=True,
        compute="_compute_total_liability",
        store=True,
    )
    total_liability_extrapolation = fields.Float(
        string="Extrapolation Total Liability",
        compute="_compute_total_liability",
        store=True,
    )
    other_base_amount = fields.Float(
        string="Other Base Amount",
        default=0.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    base_amount = fields.Selection(
        string="Base Amount",
        selection=[
            ("total_asset", "Total Asset"),
            ("net_asset", "Net Asset"),
            ("revenue", "Revenue"),
            ("cost_of_revenue", "Cost of Revenue"),
            ("ebt", "EBT"),
            ("ebitda", "EBITDA"),
            ("total_liability", "Total Liability"),
            ("other_base_amount", "Other Base Amount"),
        ],
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
        default=0.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    overall_materiality = fields.Float(
        string="Overall Materiality",
        compute="_compute_materiality",
        store=True,
    )
    overall_materiality_extrapolation = fields.Float(
        string="Extrapolation Overall Materiality",
        compute="_compute_materiality",
        store=True,
    )
    overall_materiality_consideration = fields.Text(
        string="Overall Materiality Consideration",
    )
    performance_materiality_percentage = fields.Float(
        string="Performance Materiality Percentage",
        default=0.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    performance_materiality = fields.Float(
        string="Performance Materiality",
        compute="_compute_materiality",
        store=True,
    )
    performance_materiality_extrapolation = fields.Float(
        string="Extrapolation Performance Materiality",
        compute="_compute_materiality",
        store=True,
    )
    performance_materiality_consideration = fields.Text(
        string="Performence Materiality Consideration",
    )
    tolerable_misstatement_percentage = fields.Float(
        string="Tolerable Misstatement Percentage",
        default=0.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tolerable_misstatement = fields.Float(
        string="Tolerable Misstatement",
        compute="_compute_materiality",
        store=True,
    )
    tolerable_misstatement_extrapolation = fields.Float(
        string="Extrapolation Tolerable Misstatement",
        compute="_compute_materiality",
        store=True,
    )
    tolerable_misstatement_consideration = fields.Text(
        string="Tolerable Misstatement Consideration",
    )

    status_id = fields.Many2one(
        string="Status",
        comodel_name="accountant.general_audit_index_a210_status",
        required=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion",
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
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
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
    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountantGeneralAuditIndexA210, self)
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
        _super = super(AccountantGeneralAuditIndexA210, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_valid()

    @api.multi
    def restart_validation(self):
        _super = super(AccountantGeneralAuditIndexA210, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()
