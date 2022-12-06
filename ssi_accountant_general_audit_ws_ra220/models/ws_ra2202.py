# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA2202(models.Model):
    _name = "ws_ra2202"
    _description = "General Audit WS RA.220.2"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra220.worksheet_type_ra2202"

    business_process_ids = fields.Many2many(
        string="Business Process",
        comodel_name="accountant.business_process",
        related="general_audit_id.business_process_ids",
    )
    control_risk_ids = fields.One2many(
        string="Control Risk",
        comodel_name="ws_ra2202.control_risk",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_control_risk_ids(self):
        self.update({"control_risk_ids": [(5, 0, 0)]})
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
            self.update({"control_risk_ids": result})
