# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class Project(models.Model):
    _inherit = "project.project"

    accountant_service_id = fields.Many2one(
        string="Accountant Service",
        comodel_name="accountant.service",
    )
