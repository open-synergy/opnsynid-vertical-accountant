# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA110(models.Model):
    _name = "ws_rr110"
    _description = "General Audit WS RA.110"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_rr110.worksheet_type_rr110"

    balance_type = fields.Selection(
        string="Balance Type",
        selection=[
            ("interim", "Interim"),
            ("home", "Home Statement"),
        ],
        default="home",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_ids = fields.One2many(
        string="Accounts",
        comodel_name="ws_rr110.account",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
