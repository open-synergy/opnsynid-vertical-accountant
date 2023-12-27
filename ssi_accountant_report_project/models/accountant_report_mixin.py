# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantReportMixin(models.AbstractModel):
    _name = "accountant.report_mixin"
    _inherit = [
        "accountant.report_mixin",
    ]

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_project_id(self):
        self.project_id = False
