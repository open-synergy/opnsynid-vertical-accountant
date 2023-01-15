# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WSRR1101Account(models.Model):
    _name = "ws_rr1101.account"
    _description = "General Audit WS RR.110.1 Account"

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
    balance_vertical_analysis = fields.Float(
        string="Balance Vertical Analysis",
        compute="_compute_vertical_analysis",
        store=True,
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="detail_id.previous_balance",
        store=True,
        currency_field="currency_id",
    )
    previous_vertical_analysis = fields.Float(
        string="Previous Vertical Analysis",
        compute="_compute_vertical_analysis",
        store=True,
    )
    percentage = fields.Float(
        string="Percentage",
        compute="_compute_vertical_analysis",
        store=True,
    )
    year_end_prediction = fields.Monetary(
        string="Year End Prediction",
        currency_field="currency_id",
    )
    year_end_prediction_percentage = fields.Float(
        string="Year End Prediction Percentage",
        compute="_compute_vertical_analysis",
        store=True,
    )
    year_end_detail_control = fields.Monetary(
        string="Year End Detail Control",
        currency_field="currency_id",
    )
    year_end_detail_control_percentage = fields.Float(
        string="Year End Detail Control Percentage",
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
        "year_end_prediction",
        "year_end_detail_control",
    )
    def _compute_vertical_analysis(self):
        for record in self:
            vertical_analysis = (
                previous_vertical_analysis
            ) = (
                percentage
            ) = (
                year_end_prediction_percentage
            ) = year_end_detail_control_percentage = 0.0
            worksheet = record.worksheet_id
            try:
                vertical_analysis = record.balance / worksheet.balance
            except ZeroDivisionError:
                vertical_analysis = 0.0

            try:
                previous_vertical_analysis = (
                    record.previous_balance / worksheet.previous_balance
                )
            except ZeroDivisionError:
                previous_vertical_analysis = 0.0

            try:
                percentage = record.balance / record.previous_balance
            except ZeroDivisionError:
                percentage = 0.0

            try:
                year_end_prediction_percentage = (
                    record.balance / record.year_end_prediction
                )
            except ZeroDivisionError:
                year_end_prediction_percentage = 0.0

            try:
                year_end_detail_control_percentage = (
                    record.balance / record.year_end_detail_control
                )
            except ZeroDivisionError:
                year_end_detail_control_percentage = 0.0

            record.balance_vertical_analysis = vertical_analysis
            record.previous_vertical_analysis = previous_vertical_analysis
            record.percentage = percentage
            record.year_end_prediction_percentage = year_end_prediction_percentage
            record.year_end_detail_control_percentage = (
                year_end_detail_control_percentage
            )
