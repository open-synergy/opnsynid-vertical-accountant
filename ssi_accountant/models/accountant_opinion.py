# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountantOpinion(models.Model):
    _name = "accountant.opinion"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Opinion"

    name = fields.Char(
        string="Accountant Opinion",
    )
