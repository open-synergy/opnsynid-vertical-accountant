# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantTrialBalanceComputationItem(models.Model):
    _name = "accountant.trial_balance_computation_item"
    _description = "Accountant Trial Balance Computation Item"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    description = fields.Text(
        string="Description",
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
        string="Default Python Code",
        required=True,
        default="result = result_extrapolation = result_previous = 0.0",
    )
