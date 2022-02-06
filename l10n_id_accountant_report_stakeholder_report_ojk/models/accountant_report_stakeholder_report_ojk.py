# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountantReportStakeholderReportOjk(models.Model):
    _name = "accountant.report_stakeholder_report_ojk"
    _inherit = ["accountant.report_stakeholder_report"]
    _description = "Accountat Report Stakeholder Report - OJK"
    _table = "accountant_report_stakeholder_report"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "l10n_id_accountant_report_stakeholder_report_ojk."
            "report_stakeholder_report_ojk"
        ).id

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        type_id = (
            self.env.ref(
                "l10n_id_accountant_report_stakeholder_report_ojk."
                "report_stakeholder_report_ojk",
                False,
            )
            and self.env.ref(
                "l10n_id_accountant_report_stakeholder_report_ojk."
                "report_stakeholder_report_ojk"
            )
            or self.env["accountant.report_stakeholder_report_type"]
        )
        args.append(("type_id", "=", type_id.id))
        return super(AccountantReportStakeholderReportOjk, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count
        )
