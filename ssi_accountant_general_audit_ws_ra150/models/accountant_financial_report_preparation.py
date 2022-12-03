# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import models


class AccountantFinancialReportPreparation(models.Model):
    _name = "accountant.financial_report_preparation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant - Financial Report Preparation"
