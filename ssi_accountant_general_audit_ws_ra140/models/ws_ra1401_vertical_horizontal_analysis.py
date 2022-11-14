# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS1401VerticalHorizontalAnalysis(models.Model):
    _name = "ws_ra1401.vertical_horizontal_analysis"
    _description = "General Audit WS RA.140.1 Vertical Horizontal Analysis"

    worksheet_id = fields.Many2one(
        string="# RA.140.1",
        comodel_name="ws_ra1401",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )

    computation_item_id = fields.Many2one(
        string="Base Figure Computation Item",
        comodel_name="accountant.trial_balance_computation_item",
    )

    @api.depends(
        "computation_item_id",
        "worksheet_id.general_audit_id",
    )
    def _compute_computation_item(self):
        Computation = self.env["accountant.general_audit_computation"]
        for record in self:
            result = False
            ws = record.worksheet_id
            if ws.general_audit_id and record.computation_item_id:
                criteria = [
                    ("general_audit_id", "=", ws.general_audit_id.id),
                    ("computation_item_id", "=", record.computation_item_id.id),
                ]
                computations = Computation.search(criteria)
                if len(computations) > 0:
                    result = computations[0]
            record.general_audit_computation_item_id = result

    general_audit_computation_item_id = fields.Many2one(
        string="General Audit Computation",
        comodel_name="accountant.general_audit_computation",
        compute="_compute_computation_item",
        store=True,
    )
    interim_base_figure = fields.Float(
        string="Interim Base Figure",
        related="general_audit_computation_item_id.interim_amount",
        store=True,
    )
    extrapolation_base_figure = fields.Float(
        string="Extrapolation Base Figure",
        related="general_audit_computation_item_id.extrapolation_amount",
        store=True,
    )
    previous_base_figure = fields.Float(
        string="Previous Base Figure",
        related="general_audit_computation_item_id.previous_amount",
        store=True,
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="standard_detail_id.interim_balance",
        store=True,
    )
    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related="standard_detail_id.extrapolation_balance",
        store=True,
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
    )

    @api.depends(
        "interim_base_figure",
        "extrapolation_base_figure",
        "previous_base_figure",
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_vertical(self):
        for record in self:
            interim = extrapolation = previous = 0.0

            if record.interim_base_figure != 0.0:
                interim = (record.interim_balance / record.interim_base_figure) * 100.0

            if record.extrapolation_base_figure != 0.0:
                extrapolation = (
                    record.extrapolation_balance / record.extrapolation_base_figure
                ) * 100.0

            if record.previous_base_figure != 0.0:
                previous = (
                    record.previous_balance / record.previous_base_figure
                ) * 100.0

            record.interim_vertical_analysis = interim
            record.extrapolation_vertical_analysis = extrapolation
            record.previous_vertical_analysis = previous

    interim_vertical_analysis = fields.Float(
        string="Interim Vertical Analysis",
        compute="_compute_vertical",
        store=True,
    )
    extrapolation_vertical_analysis = fields.Float(
        string="Extrapolation Vertical Analysis",
        compute="_compute_vertical",
        store=True,
    )
    previous_vertical_analysis = fields.Float(
        string="Previous Vertical Analysis",
        compute="_compute_vertical",
        store=True,
    )

    @api.depends(
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_horizontal(self):
        for record in self:
            extrapolation_change = interim_change = 0.0
            extrapolation_change_percent = interim_change_percent = 0.0
            if record.standard_detail_id:
                extrapolation_change = (
                    record.extrapolation_balance - record.previous_balance
                )
                interim_change = record.interim_balance - record.previous_balance

            if record.previous_balance != 0.0:
                extrapolation_change_percent = (
                    extrapolation_change / record.previous_balance
                ) * 100.0
                interim_change_percent = (
                    interim_change / record.previous_balance
                ) * 100.0

            record.extrapolation_change = extrapolation_change
            record.interim_change = interim_change
            record.extrapolation_change_percent = extrapolation_change_percent
            record.interim_change_percent = interim_change_percent

    extrapolation_change = fields.Monetary(
        string="Extrapolation Change",
        compute="_compute_horizontal",
        store=True,
    )
    extrapolation_change_percent = fields.Float(
        string="Extrapolation Change (%)",
        compute="_compute_horizontal",
        store=True,
    )
    interim_change = fields.Monetary(
        string="Interim Change",
        compute="_compute_horizontal",
        store=True,
    )
    interim_change_percent = fields.Float(
        string="Interim Change (%)",
        compute="_compute_horizontal",
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    vertical_need_attention = fields.Boolean(
        string="Vertical Need Attention",
        default=False,
    )
    horizontal_need_attention = fields.Boolean(
        string="Horizontal Need Attention",
        default=False,
    )
    explanation = fields.Char(
        string="Explanation",
    )
