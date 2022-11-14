# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA1402(models.Model):
    _name = "ws_ra1402"
    _description = "General Audit WS RA.140.2"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra140.worksheet_type_ra1402"

    ratio_ids = fields.One2many(
        string="Ratio Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
    )
    liquidity_ratio_ids = fields.One2many(
        string="Liquidity Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("computation_item_id.category", "=", "liquidity"),
        ],
    )
    activity_ratio_ids = fields.One2many(
        string="Activity Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("computation_item_id.category", "=", "activity"),
        ],
    )
    solvency_ratio_ids = fields.One2many(
        string="Solvency Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("computation_item_id.category", "=", "solvency"),
        ],
    )
    profitability_ratio_ids = fields.One2many(
        string="Profitability Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("computation_item_id.category", "=", "profitability"),
        ],
    )

    @api.onchange("general_audit_id")
    def onchange_ratio_ids(self):
        self.update({"ratio_ids": [(5, 0, 0)]})
        if self.general_audit_id:
            result = []
            for computation in self.general_audit_id.computation_ids:
                result.append(
                    (
                        0,
                        0,
                        {
                            "general_audit_computation_item_id": computation.id,
                        },
                    )
                )
            self.update({"ratio_ids": result})
