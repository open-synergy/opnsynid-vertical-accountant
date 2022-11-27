# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA1204(models.Model):
    _name = "ws_ra1204"
    _description = "General Audit WS RA.120.4"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra120.worksheet_type_ra1204"

    extrapolation_adjustment_ids = fields.One2many(
        string="Extrapolation Adjustment",
        comodel_name="ws_ra1204.extrapolation_adjustment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_extrapolation_adjustment_ids(self):
        self.update({"extrapolation_adjustment_ids": [(5, 0, 0)]})
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
            self.update({"extrapolation_adjustment_ids": result})
