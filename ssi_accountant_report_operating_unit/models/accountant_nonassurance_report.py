# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class NonassuranceReport(models.Model):
    _name = "accountant.nonassurance_report"
    _inherit = [
        "accountant.nonassurance_report",
        "mixin.single_operating_unit",
    ]
