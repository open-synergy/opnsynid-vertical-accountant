# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA140(models.Model):
    _name = "ws_ra140"
    _description = "General Audit WS RA.140"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra140.worksheet_type_ra140"

    conclusion_ids = fields.One2many(
        string="Conclusion",
        comodel_name="ws_ra140.analytic_procedure_conclusion",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
