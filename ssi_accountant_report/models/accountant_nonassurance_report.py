# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import models


class AccountantNonassuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = ["accountant.report_mixin"]
    _description = "Accountant Non-Assurance Report"
