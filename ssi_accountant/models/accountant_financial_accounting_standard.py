# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountantFinancialAccountingStandard(models.Model):
    _name = "accountant.financial_accounting_standard"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Financial Accounting Standard"

    name = fields.Char(
        string="Financial Accounting Standard",
    )
