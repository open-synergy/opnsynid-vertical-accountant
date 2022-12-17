# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _inherit = "accountant.general_audit_standard_detail"

    business_process_id = fields.Many2one(
        string="Business Process",
        comodel_name="accountant.business_process",
        required=False,
        ondelete="restrict",
    )
    inherent_risk = fields.Selection(
        string="Inherent Risk",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    significant_risk = fields.Boolean(
        string="Significant Risk",
    )
