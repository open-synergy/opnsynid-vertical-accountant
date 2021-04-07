# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientTrialBalanceDetail(models.Model):
    _name = "accountant.client_trial_balance_detail"
    _description = "Accountant Client Trial Balance Detail"
    _order = "sequence, trial_balance_id, id"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        required=True,
    )
    balance = fields.Float(
        string="Balance",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        required=True,
    )
    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
    )
