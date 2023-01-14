# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WSRR1101AccountAcomparison(models.Model):
    _name = "ws_rr1101.account_comparison"
    _description = "General Audit WS RR.110.1 Account Comparison"

    worksheet_id = fields.Many2one(
        string="# RR.110.1",
        comodel_name="ws_rr1101",
        required=True,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        string="Currency",
        related="worksheet_id.currency_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="detail_id.sequence",
        store=True,
    )
    detail_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.general_audit_detail",
        required=True,
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
    balance_percentage = fields.Float(
        string="Balance Percentage",
        compute="_compute_vertical_analysis",
        store=True,
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="detail_id.previous_balance",
        store=True,
        currency_field="currency_id",
    )
    previous_percentage = fields.Float(
        string="Previous Percentage",
        compute="_compute_vertical_analysis",
        store=True,
    )
    conclusion = fields.Char(
        string="Conclusion",
    )

    @api.depends(
        "worksheet_id.balance_type",
        "detail_id",
        "detail_id.interim_balance",
        "detail_id.home_statement_balance",
    )
    def _compute_balance(self):
        for record in self:
            result = 0.0
            worksheet = record.worksheet_id
            if worksheet.balance_type == "interim":
                result = record.detail_id.interim_balance
            else:
                result = record.detail_id.home_statement_balance
            record.balance = result

    @api.depends(
        "worksheet_id.balance",
        "worksheet_id.previous_balance",
        "balance",
        "previous_balance",
    )
    def _compute_vertical_analysis(self):
        for record in self:
            current_percentage = previous_percentage = 0.0
            worksheet = record.worksheet_id
            try:
                current_percentage = record.balance / worksheet.balance
            except ZeroDivisionError:
                current_percentage = 0.0

            try:
                previous_percentage = (
                    record.previous_balance / worksheet.previous_balance
                )
            except ZeroDivisionError:
                previous_percentage = 0.0

            record.current_percentage = current_percentage
            record.previous_percentage = previous_percentage
