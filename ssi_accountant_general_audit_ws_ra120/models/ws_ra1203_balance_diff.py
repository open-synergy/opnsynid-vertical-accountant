# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS1203BalanceDiff(models.Model):
    _name = "ws_ra1203.balance_diff"
    _description = "General Audit WS RA.120.3 Balance Diff"

    worksheet_id = fields.Many2one(
        string="# RA.120.3",
        comodel_name="ws_ra1203",
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
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="standard_detail_id.interim_opening_balance",
        store=True,
        currency_field="currency_id",
    )
    interim_gl_balance = fields.Monetary(
        string="Interim GL Balance",
        currency_field="currency_id",
    )
    interim_sl_balance = fields.Monetary(
        string="Interim SL Balance",
        currency_field="currency_id",
    )

    @api.depends(
        "interim_balance",
        "interim_gl_balance",
        "interim_sl_balance",
    )
    def _compute_balance_diff(self):
        for record in self:
            gl_balance_diff = sl_balance_diff = 0.0
            gl_balance_diff = record.interim_balance - record.interim_gl_balance
            sl_balance_diff = record.interim_balance - record.interim_sl_balance
            record.gl_balance_diff = gl_balance_diff
            record.sl_balance_diff = sl_balance_diff

    gl_balance_diff = fields.Monetary(
        string="TB vs. GL Balance Diff.",
        compute="_compute_balance_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
    )
    sl_balance_diff = fields.Monetary(
        string="TB vs. SL Balance Diff.",
        compute="_compute_balance_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
    )
    conclusion = fields.Text(
        string="Conclusion",
    )
