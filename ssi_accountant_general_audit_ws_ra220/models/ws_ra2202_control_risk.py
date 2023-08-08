# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA2202ControlRisk(models.Model):
    _name = "ws_ra2202.control_risk"
    _description = "RA.220.2 Control Risk"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra2202",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )
    business_process_id = fields.Many2one(
        string="Business Process",
        comodel_name="accountant.business_process",
        related="standard_detail_id.business_process_id",
        store=True,
        readonly=False,
    )
    assersion_type_ids = fields.Many2many(
        string="Assersion Types",
        comodel_name="accountant.assersion_type",
        relation="rel_control_risk_2_assersion_type",
        column1="control_risk_id",
        column2="assersion_type_id",
    )

    @api.onchange("assersion_type_ids")
    def _onchange_oassersion_type_ids(self):
        self.oassersion_type_ids = self.assersion_type_ids.ids

    oassersion_type_ids = fields.Many2many(
        string="Assersion Types",
        comodel_name="accountant.assersion_type",
        related="standard_detail_id.assersion_type_ids",
        readonly=False,
        compute=False,
    )
