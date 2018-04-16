# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    project_id = fields.Many2one(
        string=_("Project"),
        comodel_name="project.project",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("partner_id")
    def onchange_project_id(self):
        self.project_id = False
