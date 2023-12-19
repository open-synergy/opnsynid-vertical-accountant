# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import models


class AccountantAssuranceReport(models.Model):
    _name = "accountant.assurance_report"
    _inherit = [
        "accountant.assurance_report",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
