# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from datetime import datetime

from odoo import api, fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _description = "Accountant General Audit Standard Detail"
    _order = "sequence, general_audit_id, id"

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        required=True,
        ondelete="cascade",
    )

    @api.depends(
        "general_audit_id",
        "general_audit_id.home_trial_balance_id",
        "general_audit_id.interim_trial_balance_id",
        "general_audit_id.previous_trial_balance_id",
    )
    def _compute_standard_line(self):
        StandardDetail = self.env["accountant.client_trial_balance_standard_detail"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("type_id", "=", record.type_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = StandardDetail.search(criteria_home)
                if len(home_results) > 0:
                    home_result = home_results[0]

            if record.general_audit_id.interim_trial_balance_id:
                criteria_interim = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.interim_trial_balance_id.id,
                    )
                ]
                interim_results = StandardDetail.search(criteria_interim)
                if len(interim_results) > 0:
                    interim_result = interim_results[0]

            if record.general_audit_id.previous_trial_balance_id:
                criteria_previous = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.previous_trial_balance_id.id,
                    )
                ]
                previous_results = StandardDetail.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_standard_line_id = home_result
            record.interim_standard_line_id = interim_result
            record.previous_standard_line_id = previous_result

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
    )
    def _compute_standard_adjustment_id(self):
        StandardAdjustment = self.env["accountant.general_audit_adjustment"]
        for record in self:
            result = False
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("type_id", "=", record.type_id.id),
            ]
            standard_adjustments = StandardAdjustment.search(criteria)
            if len(standard_adjustments) > 0:
                result = standard_adjustments[0]
            record.standard_adjustment_id = result

    standard_adjustment_id = fields.Many2one(
        string="Standard Adjustment",
        comodel_name="accountant.general_audit_adjustment",
        readonly=True,
        compute="_compute_standard_adjustment_id",
        store=True,
    )

    home_standard_line_id = fields.Many2one(
        string="Home Statement TB Standard Line",
        comodel_name="accountant.client_trial_balance_standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    interim_standard_line_id = fields.Many2one(
        string="Interim TB Standard Line",
        comodel_name="accountant.client_trial_balance_standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    previous_standard_line_id = fields.Many2one(
        string="Previous TB Standard Line",
        comodel_name="accountant.client_trial_balance_standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=True,
    )
    home_statement_balance = fields.Monetary(
        string="Home Statement Balance",
        related="home_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )
    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related="interim_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )
    previous_balance = fields.Monetary(
        string="Extrapolation Balance",
        related="previous_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )

    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        related="standard_adjustment_id.debit",
        store=True,
        currency_field="currency_id",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        related="standard_adjustment_id.credit",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "type_id",
        "adjustment_debit",
        "adjustment_credit",
        "home_statement_balance",
    )
    def _compute_adjustment_audited_balance(self):
        for record in self:
            adjustment = audited = 0.0
            if record.type_id:
                if record.type_id.normal_balance == "dr":
                    adjustment = record.adjustment_debit - record.adjustment_credit
                else:
                    adjustment = record.adjustment_credit - record.adjustment_debit
            audited = record.home_statement_balance + adjustment
            record.audited_balance = audited
            record.adjustment_balance = adjustment

    adjustment_balance = fields.Float(
        string="Adjustment Balance",
        compute="_compute_adjustment_audited_balance",
        store=True,
    )
    audited_balance = fields.Float(
        string="Audited Balance",
        compute="_compute_adjustment_audited_balance",
        store=True,
    )

    def _get_localdict(
        self, previous_balance, balance, interim_balance, audited_balance
    ):
        self.ensure_one()
        tb = self.trial_balance_id
        date_start = (
            tb.date_start
            and datetime.strptime(str(tb.date_start), "%Y-%m-%d").date()
            or False
        )
        date_end = (
            tb.date_end
            and datetime.strptime(str(tb.date_end), "%Y-%m-%d").date()
            or False
        )
        previous_date_start = (
            tb.previous_date_start
            and datetime.strptime(str(tb.previous_date_start), "%Y-%m-%d").date()
            or False
        )
        previous_date_end = (
            tb.previous_date_end
            and datetime.strptime(str(tb.previous_date_end), "%Y-%m-%d").date()
            or False
        )
        interim_date_start = (
            tb.interim_date_start
            and datetime.strptime(str(tb.interim_date_start), "%Y-%m-%d").date()
            or False
        )
        interim_date_end = (
            tb.interim_date_end
            and datetime.strptime(str(tb.interim_date_end), "%Y-%m-%d").date()
            or False
        )
        return {
            "env": self.env,
            "document": self,
            "previous_balance": previous_balance,
            "interim_balance": interim_balance,
            "audited_balance": audited_balance,
            "balance": balance,
            "datetime": datetime,
            "date_start": date_start,
            "date_end": date_end,
            "previous_date_start": previous_date_start,
            "previous_date_end": previous_date_end,
            "interim_date_start": interim_date_start,
            "interim_date_end": interim_date_end,
        }
