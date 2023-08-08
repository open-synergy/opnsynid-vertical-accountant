# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantClientAccountType(models.Model):
    _name = "accountant.client_account_type"
    _inherit = "accountant.client_account_type"

    analytic_procedure_computation_item_id = fields.Many2one(
        string="Computation Item for Analytic Procedure",
        comodel_name="accountant.trial_balance_computation_item",
    )
