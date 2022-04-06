# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantReportMethod(models.Model):
    _name = "accountant.report_method"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Report Method"
    _order = "id"

    name = fields.Char(
        string="Method",
    )
