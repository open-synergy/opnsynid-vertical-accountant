# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _name = "accountant.client_account_type_set"
    _inherit = [
        "mixin.master_data",
    ]

    _description = "Accountant Client Account Type Set"
    _order = "id"

    name = fields.Char(
        string="Account Type Set",
    )
    detail_ids = fields.Many2many(
        string="Detail",
        comodel_name="accountant.client_account_type",
        relation="rel_accountant_type_set_2_account_type",
        column1="account_client_type_set_id",
        column2="account_client_type_id",
    )
    computation_ids = fields.One2many(
        string="Computation",
        comodel_name="accountant.client_account_type_computation_item",
        inverse_name="account_type_set_id",
        copy=True,
    )
