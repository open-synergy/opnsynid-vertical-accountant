# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class WSAudit1505(models.Model):
    _name = "ws_ra1505"
    _description = "General Audit WS RA.150.5"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra150.worksheet_type_ra1505"

    trend_business_environment_ids = fields.One2many(
        string="Similar Business Trend Understanding",
        comodel_name="ws_ra1505.trend_business_environment",
        inverse_name="worksheet_id",
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    economic_business_environment_ids = fields.One2many(
        string="National Economic Understanding",
        comodel_name="ws_ra1505.economic_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    ifrs_business_environment_ids = fields.One2many(
        string="Financial Standard Amendment Understanding",
        comodel_name="ws_ra1505.ifrs_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    regulation_business_environment_ids = fields.One2many(
        string="Regulation Change Understanding",
        comodel_name="ws_ra1505.regulation_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    technology_business_environment_ids = fields.One2many(
        string="Technology Advancement Understanding",
        comodel_name="ws_ra1505.technology_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    natural_business_environment_ids = fields.One2many(
        string="Natural Cycle Understanding",
        comodel_name="ws_ra1505.natural_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    energy_business_environment_ids = fields.One2many(
        string="Energy Availability & Cost Understanding",
        comodel_name="ws_ra1505.energy_business_environment",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
