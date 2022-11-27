# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _inherit = "accountant.general_audit_standard_detail"

    adjusted_extrapolation_balance = fields.Monetary(
        string="Adjusted Extrapolation Balance",
        currency_field="currency_id",
    )
