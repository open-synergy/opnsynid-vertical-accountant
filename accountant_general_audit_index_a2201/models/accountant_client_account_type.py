# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountType(models.Model):
    _name = "accountant.client_account_type"
    _inherit = "accountant.client_account_type"

    bottom_line_id = fields.Many2one(
        string="Bottom Line for Vertical Analysis",
        comodel_name="accountant.trial_balance_computation_item",
    )
