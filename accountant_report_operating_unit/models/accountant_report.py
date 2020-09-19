# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    @api.model
    def _default_operating_unit_id(self):
        return self.env["res.users"].operating_unit_default_get(self._uid)

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        default=lambda self: self._default_operating_unit_id(),
    )
