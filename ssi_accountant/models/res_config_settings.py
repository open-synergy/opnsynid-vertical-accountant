# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
        "abstract.config.settings",
    ]

    module_ssi_accountant_report = fields.Boolean(
        string="Accountant Report",
    )
    module_ssi_accountant_stakeholder_report = fields.Boolean(
        string="Accountant Stakeholder Report",
    )
    module_ssi_general_audit = fields.Boolean(
        string="General Audit",
    )
