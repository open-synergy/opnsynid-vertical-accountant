# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WSRR1101ComputationAcomparison(models.Model):
    _name = "ws_rr1101.computation_comparison"
    _description = "General Audit WS RR.110.1 Computation Comparison"

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
        related="computation_id.sequence",
        store=True,
    )
    computation_id = fields.Many2one(
        string="Computation",
        comodel_name="accountant.general_audit_computation",
        required=True,
    )
    balance = fields.Float(
        string="Balance",
        compute="_compute_balance",
        store=True,
    )
    balance_percentage = fields.Float(
        string="Balance Percentage",
        compute="_compute_vertical_analysis",
        store=True,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        related="computation_id.previous_amount",
        store=True,
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
        "computation_id",
        "computation_id.interim_amount",
        "computation_id.home_amount",
    )
    def _compute_balance(self):
        for record in self:
            result = 0.0
            worksheet = record.worksheet_id
            if worksheet.balance_type == "interim":
                result = record.computation_id.interim_amount
            else:
                result = record.computation_id.home_amount
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
