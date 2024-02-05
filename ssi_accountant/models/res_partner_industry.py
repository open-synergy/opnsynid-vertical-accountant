# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerIndustry(models.Model):
    _name = "res.partner.industry"
    _inherit = [
        "res.partner.industry",
    ]

    accountant_service_code = fields.Char(
        string="Accountant Service Code",
    )
