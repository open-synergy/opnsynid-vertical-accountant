# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA22021(models.Model):
    _name = "ws_ra22021"
    _description = "General Audit WS RA.220.2.1"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra220.worksheet_type_ra22021"

    business_process_ids = fields.Many2many(
        string="Allowed Business Process",
        comodel_name="accountant.business_process",
        related="general_audit_id.business_process_ids",
        store=False,
    )
    business_process_id = fields.Many2one(
        string="Business Process",
        comodel_name="accountant.business_process",
        required=True,
    )
    account_cycle_ids = fields.One2many(
        string="Account Cycle",
        comodel_name="ws_ra22021.account_cycle",
        inverse_name="worksheet_id",
    )
    cycle_detail_ids = fields.One2many(
        string="Cycle Detail",
        comodel_name="ws_ra22021.cycle_detail",
        inverse_name="worksheet_id",
    )

    @api.onchange("general_audit_id", "business_process_id")
    def onchange_control_risk_ids(self):
        self.update({"account_cycle_ids": [(5, 0, 0)]})
        StdDetail = self.env["accountant.general_audit_standard_detail"]

        if self.general_audit_id and self.business_process_id:
            result = []
            criteria = [
                ("business_process_id", "=", self.business_process_id.id),
                ("general_audit_id", "=", self.general_audit_id.id),
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
