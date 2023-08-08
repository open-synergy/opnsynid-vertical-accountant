# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantTrialBalanceComputationItem(models.Model):
    _name = "accountant.trial_balance_computation_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Trial Balance Computation Item"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    category = fields.Selection(
        string="Category",
        selection=[
            ("summary", "Trial Balance Summary"),
            ("liquidity", "Liquidity Ratio"),
            ("activity", "Activity Ratio"),
            ("solvency", "Solvency Ratio"),
            ("profitability", "Profitability Ratio"),
        ],
        required=True,
        default="summary",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result = result_extrapolation = result_previous = 0.0",
    )
