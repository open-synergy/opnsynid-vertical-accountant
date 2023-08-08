# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantAuditStandardItem(models.Model):
    _name = "accountant.audit_standard_item"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Audit Standard Item"
    _show_code_on_display_name = True

    standard_id = fields.Many2one(
        string="Audit Standard",
        comodel_name="accountant.audit_standard",
        required=True,
    )
