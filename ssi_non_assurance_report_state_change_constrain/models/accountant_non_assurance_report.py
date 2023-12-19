# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import models


class AccountantNonAssuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = [
        "accountant.nonassurance_report",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
