# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantClientAccountGroup(models.Model):
    _name = "accountant.client_account_group"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Account Group"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
