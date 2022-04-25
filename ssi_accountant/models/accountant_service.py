# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountantService(models.Model):
    _name = "accountant.service"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Service"

    name = fields.Char(
        string="Accountant Service",
    )
