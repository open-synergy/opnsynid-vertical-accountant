# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantClientAccountTypeComputationItem(models.Model):
    _name = "accountant.client_account_type_computation_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Account Type Computation Item"

    name = fields.Char(
        required=False,
    )
    code = fields.Char(
        required=False,
    )
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
        string="Python Code",
        default="result = 0.0",
    )

    @api.onchange(
        "computation_id",
    )
    def onchange_phyton_code(self):
        self.phyton_code = "result = 0.0"
        if self.computation_id:
            computation = self.computation_id
            self.phyton_code = computation.python_code
