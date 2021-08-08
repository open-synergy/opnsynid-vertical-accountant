# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _name = "accountant.client_account_type_set"
    _inherit = "accountant.client_account_type_set"

    total_asset_python_code = fields.Text(
        string="Python Code for Total Asset",
    )
    net_asset_python_code = fields.Text(
        string="Python Code for Net Asset",
    )
    revenue_python_code = fields.Text(
        string="Python Code for Revenue",
    )
    cost_of_revenue_python_code = fields.Text(
        string="Python Code for Cost of Revenue",
    )
    ebt_python_code = fields.Text(
        string="Python Code for EBT",
    )
    ebitda_python_code = fields.Text(
        string="Python Code for EBITDA",
    )
    total_liability_python_code = fields.Text(
        string="Python Code for Total Liability",
    )
