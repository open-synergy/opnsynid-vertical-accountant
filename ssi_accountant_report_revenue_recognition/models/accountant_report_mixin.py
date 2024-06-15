# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantReportMixin(models.AbstractModel):
    _inherit = "accountant.report_mixin"

    pob_id = fields.Many2one(
        string="POB",
        required=False,
        comodel_name="service_contract.performance_obligation",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("partner_id")
    def onchange_pob_id(self):
        self.pob_id = False
