# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS1203ExtrapolationAdjustment(models.Model):
    _name = "ws_ra1204.extrapolation_adjustment"
    _description = "General Audit WS RA.120.4 Extrapolation Adjustment"

    worksheet_id = fields.Many2one(
        string="# RA.120.4",
        comodel_name="ws_ra1204",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="type_id.sequence",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="worksheet_id.currency_id",
        store=True,
    )
    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related="standard_detail_id.extrapolation_balance",
        store=True,
        currency_field="currency_id",
    )
    extrapolation_adjustment = fields.Monetary(
        string="Extrapolation Adjustment",
        currency_field="currency_id",
    )

    @api.onchange(
        "extrapolation_balance",
        "extrapolation_adjustment",
    )
    def _compute_adjusted_extrapolation_balance(self):
        for record in self:
            result = record.extrapolation_balance + record.extrapolation_adjustment
            record.adjusted_extrapolation_balance = result

    adjusted_extrapolation_balance = fields.Monetary(
        string="Adjusted Extrapolation Balance",
        currency_field="currency_id",
        related="standard_detail_id.adjusted_extrapolation_balance",
        readonly=True,
        store=True,
        compute="_compute_adjusted_extrapolation_balance",
    )
    conclusion = fields.Text(
        string="Conclusion",
    )
