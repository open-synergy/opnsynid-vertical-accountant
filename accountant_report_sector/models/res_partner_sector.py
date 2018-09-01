# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartnerSector(models.Model):
    _inherit = "res.partner.sector"

    accountant_service_code = fields.Char(
        string="Code for Accountant Service",
    )
