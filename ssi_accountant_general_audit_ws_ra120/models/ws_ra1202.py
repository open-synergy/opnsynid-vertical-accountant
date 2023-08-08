# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA1202(models.Model):
    _name = "ws_ra1202"
    _description = "General Audit WS RA.120.2"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra120.worksheet_type_ra1202"

    balance_diff_ids = fields.One2many(
        string="Balance Diff.",
        comodel_name="ws_ra1202.balance_diff",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_balance_diff_ids(self):
        self.update({"balance_diff_ids": [(5, 0, 0)]})
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
            self.update({"balance_diff_ids": result})
