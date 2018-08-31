# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.depends(
        "id_numbers", "id_numbers.status",
        "id_numbers.category_id")
    def _compute_cpa_firm_identification(self):
        obj_identification = self.env[
            "res.partner.id_number"]
        try:
            category = self.env.ref(
                "partner_identification_cpa_firm_license."
                "partner_identification_accountant_cpa_firm_license")

            for partner in self:
                criteria = [
                    ("category_id", "=", category.id),
                    ("partner_id", "=", partner.id),
                    ("status", "=", "open"),
                ]
                identifications = obj_identification.search(criteria, limit=1)
                if len(identifications) > 0:
                    partner.cpa_firm_identification_id = identifications[0].id
        except:
            for partner in self:
                partner.cpa_firm_identification_id = False

    cpa_firm_identification_id = fields.Many2one(
        string="CPA Firm Identification",
        comodel_name="res.partner.id_number",
        compute="_compute_cpa_firm_identification",
        store=True,
    )
