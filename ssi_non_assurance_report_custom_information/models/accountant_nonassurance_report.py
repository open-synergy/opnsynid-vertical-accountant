# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class AccountantNonAssuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = [
        "accountant.nonassurance_report",
        "mixin.custom_info",
    ]
    _custom_info_create_page = True
