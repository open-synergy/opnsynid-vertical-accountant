# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA230(models.Model):
    _name = "ws_ra230"
    _description = "General Audit WS RA.230"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra230.worksheet_type_ra230"

    risk_material_missstatement = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        readonly=True,
        required=False,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    auditor_respons = fields.Text(
        string="Auditor Respons",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    account_assersion_romm_ids = fields.One2many(
        string="Account Assersion Level ROMM",
        comodel_name="ws_ra230.account_assersion_level_romm",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_account_inherent_risk_ids(self):
        self.update({"account_assersion_romm_ids": [(5, 0, 0)]})
        if self.general_audit_id:
            result = []
            for detail in self.general_audit_id.standard_detail_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "standard_detail_id": detail.id,
                        },
                    )
                )
            self.update({"account_assersion_romm_ids": result})
