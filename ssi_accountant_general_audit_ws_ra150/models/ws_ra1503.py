# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAudit1503(models.Model):
    _name = "ws_ra1503"
    _description = "General Audit WS RA.150.3"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra150.worksheet_type_ra1503"

    business_process_ids = fields.One2many(
        string="Business Process",
        comodel_name="ws_ra1503.business_process",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    expert_ids = fields.One2many(
        string="Experts",
        comodel_name="ws_ra1503.expert",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_significant_information_ids = fields.One2many(
        string="Other Significant Information",
        comodel_name="ws_ra1503.other_significant_information",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    previous_significant_information_ids = fields.One2many(
        string="Previous Significant Information",
        comodel_name="ws_ra1503.previous_significant_information",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
