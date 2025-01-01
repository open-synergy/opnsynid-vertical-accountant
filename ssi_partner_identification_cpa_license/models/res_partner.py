# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    cpa_license = fields.Char(
        string="CPA License",
        compute=lambda s: s._compute_identification("cpa_license", "cpa_license"),
        search=lambda s, *a: s._search_identification("cpa_license", *a),
    )
