# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeComputationItem(models.Model):
    _name = "accountant.client_account_type_computation_item"
    _description = "Accountant Client Account Type Computation Item"

    account_type_set_id = fields.Many2one(
        string="Account Type Set",
        comodel_name="accountant.client_account_type_set",
        required=True,
    )
    computation_id = fields.Many2one(
        string="Computation",
        comodel_name="accountant.trial_balance_computation_item",
        required=True,
    )
    phyton_code = fields.Text(
        string="Phyton Code",
        default="result = 0.0",
    )
