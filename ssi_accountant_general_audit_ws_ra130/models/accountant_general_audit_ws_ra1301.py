# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantGeneralWSAuditRA1301(models.Model):
    _name = "accountant.general_audit_ws_ra1301"
    _description = "General Audit WS RA.130.1"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra130.worksheet_type_ra1301"

    worksheet_ra130_id = fields.Many2one(
        string="# RA.130",
        comodel_name="accountant.general_audit_ws_ra130",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    materiality_type = fields.Selection(
        string="Materiality Type",
        selection=[
            ("om", "Overall Materiality"),
            ("pm", "Performance Materiality"),
        ],
        required=False,
        default="pm",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    materiality_mapping_ids = fields.One2many(
        string="Materiality Mapping",
        comodel_name="accountant.general_audit_ws_ra1301_materiality_mapping",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_materiality_mapping_ids(self):
        self.update({"materiality_mapping_ids": [(5, 0, 0)]})
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
            self.update({"materiality_mapping_ids": result})
