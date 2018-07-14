# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    @api.multi
    @api.depends(
        "assurance_report_ids",
        "non_assurance_report_ids",
    )
    def _compute_accountant_report(self):
        for project in self:
            project.assurance_report_count = len(project.
                                                 assurance_report_ids)
            project.non_assurance_report_count = len(project.
                                                     non_assurance_report_ids)

    assurance_report_ids = fields.One2many(
        string="Assurance Report",
        comodel_name="accountant.report",
        inverse_name="project_id",
        domain=[
            ('assurance', '=', True),
        ],
    )
    assurance_report_count = fields.Integer(
        string="Assurance Report Count",
        compute="_compute_accountant_report",
        store=False,
    )
    non_assurance_report_ids = fields.One2many(
        string="Non-Assurance Report",
        comodel_name="accountant.report",
        inverse_name="project_id",
        domain=[
            ('assurance', '=', False),
        ],
    )
    non_assurance_report_count = fields.Integer(
        string="Non-Assurance Report Count",
        compute="_compute_accountant_report",
        store=False,
    )
