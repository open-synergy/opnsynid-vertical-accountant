# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantClientAccountType(models.Model):
    _name = "accountant.client_account_type"
    _inherit = ["mixin.master_data"]
    _description = "Accountant Client Account Type"
    _order = "sequence, id"

    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="accountant.client_account_group",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
        required=True,
        default="dr",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result = document.balance",
    )
