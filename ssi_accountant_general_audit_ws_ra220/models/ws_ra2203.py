# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA2203(models.Model):
    _name = "ws_ra2203"
    _description = "General Audit WS RA.220.3"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra220.worksheet_type_ra2203"

    account_cycle_ids = fields.One2many(
        string="Account Cycle",
        comodel_name="ws_ra2203.account_cycle",
        inverse_name="worksheet_id",
    )

    @api.onchange("general_audit_id")
    def onchange_account_cycle_ids(self):
        self.update({"account_cycle_ids": [(5, 0, 0)]})
        StdDetail = self.env["accountant.general_audit_standard_detail"]

        if self.general_audit_id:
            result = []
            criteria = [
                ("general_audit_id", "=", self.general_audit_id.id),
                (
                    "significant_risk",
                    "=",
                    True,
                ),
            ]
            for detail in StdDetail.search(criteria):
                result.append(
                    (
                        0,
                        0,
                        {
                            "standard_detail_id": detail.id,
                        },
                    )
                )
            self.update({"account_cycle_ids": result})
