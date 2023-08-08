# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantGeneralAudit(models.Model):
    _name = "accountant.general_audit"
    _inherit = "accountant.general_audit"

    @api.depends("obusiness_process_ids", "obusiness_process_ids.business_process_id")
    def _compute_business_process_ids(self):
        for record in self:
            result = record.obusiness_process_ids.business_process_id.mapped("id")
            record.business_process_ids = result

    business_process_ids = fields.Many2many(
        string="Business Process",
        comodel_name="accountant.business_process",
        relation="rel_general_audit_2_business_process",
        column1="general_audit_id",
        column2="business_process_id",
        compute="_compute_business_process_ids",
        store=True,
    )
    obusiness_process_ids = fields.One2many(
        string="Business Process",
        comodel_name="ws_ra1503.business_process",
        inverse_name="general_audit_id",
    )
