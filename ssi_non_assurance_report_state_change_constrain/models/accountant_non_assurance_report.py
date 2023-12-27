# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import api, models


class AccountantNonAssuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = [
        "accountant.nonassurance_report",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True

    @api.onchange("service_id")
    def onchange_status_check_template_id(self):
        self.status_check_template_id = self._get_template_status_check()
        self.onchange_status_check_ids()

    @api.onchange(
        "status_check_template_id",
    )
    def onchange_state_change_constrain_template_id(self):
        self.state_change_constrain_template_id = False
        if self.status_check_template_id:
            template_id = self._get_template_state_change()
            self.state_change_constrain_template_id = template_id
