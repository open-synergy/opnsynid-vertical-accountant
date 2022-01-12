# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    stakeholder_report_ids = fields.Many2many(
        string="Accountant Reports",
        comodel_name="accountant.report",
        relation="rel_stakeholder_report_2_accountant_report",
        column1="stakeholder_report_id",
        column2="accountant_report_id",
    )
