# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantReportStakeholderReportType(models.Model):
    _name = "accountant.report_stakeholder_report_type"
    _inherit = ["mixin.master_data"]
    _description = "Accounting Report Stakeholder Report Type"
    _order = "id"

    domain = fields.Text(string="Domain", required=True, default="[]")
