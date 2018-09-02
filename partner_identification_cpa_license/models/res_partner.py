# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    cpa_license = fields.Char(
        string="CPA License",
        compute=lambda s: s._compute_identification(
            "cpa_license", "accountant_cpa_license"),
        search=lambda s, *a: s._search_identification(
            "accountant_cpa_license", *a),
    )
