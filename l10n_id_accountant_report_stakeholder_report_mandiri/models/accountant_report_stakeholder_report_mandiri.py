# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountantReportStakeholderReportMandiri(models.Model):
    _name = "accountant.report_stakeholder_report_mandiri"
    _inherit = ["accountant.report_stakeholder_report"]
    _description = "Accountat Report Stakeholder Report - Bank Mandiri"
    _table = "accountant_report_stakeholder_report"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "l10n_id_accountant_report_stakeholder_report_mandiri."
            "report_stakeholder_report_mandiri"
        ).id

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        type_id = (
            self.env.ref(
                "l10n_id_accountant_report_stakeholder_report_mandiri."
                "report_stakeholder_report_mandiri",
                False,
            )
            and self.env.ref(
                "l10n_id_accountant_report_stakeholder_report_mandiri."
                "report_stakeholder_report_mandiri"
            )
            or self.env["accountant.report_stakeholder_report_type"]
        )
        args.append(("type_id", "=", type_id.id))
        return super(AccountantReportStakeholderReportMandiri, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count
        )
