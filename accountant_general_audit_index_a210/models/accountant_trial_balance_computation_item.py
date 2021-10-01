# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantTrialBalanceComputationItem(models.Model):
    _name = "accountant.trial_balance_computation_item"
    _inherit = "accountant.trial_balance_computation_item"

    materiality_ok = fields.Boolean(
        string="Can Be Used for Mateliarity Analysis",
        default=False,
    )
