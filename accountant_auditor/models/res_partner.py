# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    auditor = fields.Boolean(
        string="Auditor",
    )

    @api.onchange("is_company")
    def onchange_auditor(self):
        if self.is_company:
            self.auditor = False
