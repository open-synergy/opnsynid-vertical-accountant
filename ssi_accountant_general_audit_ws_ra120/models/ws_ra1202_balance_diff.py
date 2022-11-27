# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WS1202BalanceDiff(models.Model):
    _name = "ws_ra1202.balance_diff"
    _description = "General Audit WS RA.120.2 Balance Diff"

    worksheet_id = fields.Many2one(
        string="# RA.120.2",
        comodel_name="ws_ra1202",
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
    interim_opening_balance = fields.Monetary(
        string="Interim Opening Balance",
        related="standard_detail_id.interim_opening_balance",
        store=True,
        currency_field="currency_id",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "interim_opening_balance",
        "previous_balance",
    )
    def _compute_balance_diff(self):
        for record in self:
            result = record.interim_opening_balance - record.previous_balance
            record.balance_diff = result

    balance_diff = fields.Monetary(
        string="Balance Diff.",
        compute="_compute_balance_diff",
        compute_sudo=True,
        store=True,
        currency_field="currency_id",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.balance_diff_category",
    )
    conclusion = fields.Text(
        string="Conclusion",
    )
