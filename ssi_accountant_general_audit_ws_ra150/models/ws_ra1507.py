# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAudit1507(models.Model):
    _name = "ws_ra1507"
    _description = "General Audit WS RA.150.7"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra150.worksheet_type_ra1507"

    financial_report_preparation_ids = fields.One2many(
        string="Financial Report Preparation",
        comodel_name="ws_ra1507.financial_report_preparation",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_financial_report_preparation_ids(self):
        self.update({"financial_report_preparation_ids": [(5, 0, 0)]})
        PreparationItem = self.env["accountant.financial_report_preparation"]
        if self.general_audit_id:
            result = []
            for preparation in PreparationItem.search([]):
                result.append(
                    (
                        0,
                        0,
                        {
                            "preparation_item_id": preparation.id,
                        },
                    )
                )
            self.update({"financial_report_preparation_ids": result})
