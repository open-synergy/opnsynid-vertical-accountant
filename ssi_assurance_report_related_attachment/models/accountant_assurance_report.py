# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class AccountantAssuranceReport(models.Model):
    _name = "accountant.assurance_report"
    _inherit = [
        "accountant.assurance_report",
        "mixin.related_attachment",
    ]
    _related_attachment_create_page = True

    @api.onchange("service_id")
    def onchange_related_attachment_template_id(self):
        self.related_attachment_template_id = self._get_template_related_attachment()
        self.onchange_related_attachment_ids()
