# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResConfig(models.TransientModel):
    _name = "accountant.config_setting"
    _inherit = "res.config.settings"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    module_accountant_partner_arrangement = fields.Boolean(
        string="Partner Arrangement",
    )
    module_accountant_report = fields.Boolean(
        string="Accountant Report",
    )
    module_accountant_report_quality_control = fields.Boolean(
        string="Quality Control on Accountant Report",
    )
    module_accountant_report_project = fields.Boolean(
        string="Integrate Accountant Report - Project",
    )
