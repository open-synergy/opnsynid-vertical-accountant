# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class AccountantAssuranceReport(models.Model):
    _name = "accountant.assurance_report"
    _inherit = ["accountant.report_mixin"]
    _description = "Accountant Assurance Report"

    restatement_id = fields.Many2one(
        comodel_name="accountant.assurance_report",
    )
    opinion_id = fields.Many2one(
        string="Opinion",
        comodel_name="accountant.opinion",
        required=False,
        readonly=True,
        states={
            "ready": [
                ("readonly", False),
            ],
        },
    )

    @ssi_decorator.pre_confirm_check()
    def _01_check_opinion(self):
        self.ensure_one()
        if not self.opinion_id:
            error_message = """
                Context: Confirm document
                Database ID: %s
                Problem: No opnion selected
                Solution: Select opinion
                """ % (
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
