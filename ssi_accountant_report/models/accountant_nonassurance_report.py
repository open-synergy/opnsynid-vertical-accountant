# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class AccountantNonassuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = ["accountant.report_mixin"]
    _description = "Accountant Non-Assurance Report"

    restatement_id = fields.Many2one(
        comodel_name="accountant.nonassurance_report",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
