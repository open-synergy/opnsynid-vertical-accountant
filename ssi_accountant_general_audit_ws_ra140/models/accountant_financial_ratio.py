# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantFinancialRatio(models.Model):
    _name = "accountant.financial_ratio"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant - Financial Ratio"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result_interi = result_extrapolation = result_previous = 0.0",
    )
    category = fields.Selection(
        string="Category",
        selection=[
            ("liquidity", "Liquidity Ratio"),
            ("activity", "Activity Ratio"),
            ("solvency", "Solvency Ratio"),
            ("profitability", "Profitability Ratio"),
        ],
        required=True,
        default="summary",
    )
