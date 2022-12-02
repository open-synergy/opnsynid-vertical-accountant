# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import api, fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _inherit = "accountant.general_audit_standard_detail"

    @api.depends(
        "expert_ids",
    )
    def _compute_expert_ok(self):
        for record in self:
            result = False
            if len(record.expert_ids) > 0:
                result = True
            record.expert_ok = result

    expert_ok = fields.Boolean(
        string="Expert",
        compute="_compute_expert_ok",
        store=True,
    )
    expert_ids = fields.Many2many(
        string="Experts",
        comodel_name="ws_ra1503.expert",
        relation="rel_expert_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="expert_id",
        required=False,
    )

    @api.depends(
        "other_significant_information_ids",
    )
    def _compute_other_significant_information_ids(self):
        for record in self:
            result = False
            if len(record.other_significant_information_ids) > 0:
                result = True
            record.other_significant_information_ok = result

    other_significant_information_ok = fields.Boolean(
        string="Other Significant Information",
        compute="_compute_other_significant_information_ids",
        store=True,
    )
    other_significant_information_ids = fields.Many2many(
        string="Other Significant Informations",
        comodel_name="ws_ra1503.other_significant_information",
        relation="rel_other_sig_info_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="information_id",
    )

    @api.depends(
        "previous_significant_information_ids",
    )
    def _compute_previous_significant_information_ids(self):
        for record in self:
            result = False
            if len(record.previous_significant_information_ids) > 0:
                result = True
            record.previous_significant_information_ok = result

    previous_significant_information_ok = fields.Boolean(
        string="Previous Significant Information",
        compute="_compute_previous_significant_information_ids",
        store=True,
    )
    previous_significant_information_ids = fields.Many2many(
        string="Previous Significant Informations",
        comodel_name="ws_ra1503.previous_significant_information",
        relation="rel_prev_sig_info_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="information_id",
    )
