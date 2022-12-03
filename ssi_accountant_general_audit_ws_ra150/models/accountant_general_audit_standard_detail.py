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

    @api.depends(
        "relevant_regulation_ids",
        "relevant_regulation_ids.standard_detail_id",
    )
    def _compute_relevant_regulation_ok(self):
        for record in self:
            result = False
            if len(record.relevant_regulation_ids) > 0:
                result = True
            record.relevant_regulation_ok = result

    relevant_regulation_ok = fields.Boolean(
        string="Relevant Regulation",
        compute="_compute_relevant_regulation_ok",
        store=True,
    )
    relevant_regulation_ids = fields.One2many(
        string="Relevant Regulations",
        comodel_name="ws_ra1504.relevant_regulation_account",
        inverse_name="standard_detail_id",
    )

    @api.depends(
        "trend_business_environment_ids",
    )
    def _compute_trend_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.trend_business_environment_ids) > 0:
                result = True
            record.trend_business_environment_ok = result

    trend_business_environment_ok = fields.Boolean(
        string="Similar Business Trends",
        compute="_compute_trend_business_environment_ok",
        store=True,
    )
    trend_business_environment_ids = fields.Many2many(
        string="Similar Business Trends",
        comodel_name="ws_ra1505.trend_business_environment",
        relation="rel_trend_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "economic_business_environment_ids",
    )
    def _compute_economic_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.economic_business_environment_ids) > 0:
                result = True
            record.economic_business_environment_ok = result

    economic_business_environment_ok = fields.Boolean(
        string="National Economic",
        compute="_compute_economic_business_environment_ok",
        store=True,
    )
    economic_business_environment_ids = fields.Many2many(
        string="National Economics",
        comodel_name="ws_ra1505.economic_business_environment",
        relation="rel_economic_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "ifrs_business_environment_ids",
    )
    def _compute_ifrs_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.ifrs_business_environment_ids) > 0:
                result = True
            record.ifrs_business_environment_ok = result

    ifrs_business_environment_ok = fields.Boolean(
        string="Financial Accounting Standard Amendment",
        compute="_compute_ifrs_business_environment_ok",
        store=True,
    )
    ifrs_business_environment_ids = fields.Many2many(
        string="Financial Accounting Standard Amendments",
        comodel_name="ws_ra1505.ifrs_business_environment",
        relation="rel_ifrs_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "regulation_business_environment_ids",
    )
    def _compute_regulation_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.regulation_business_environment_ids) > 0:
                result = True
            record.regulation_business_environment_ok = result

    regulation_business_environment_ok = fields.Boolean(
        string="Regulation Change",
        compute="_compute_regulation_business_environment_ok",
        store=True,
    )
    regulation_business_environment_ids = fields.Many2many(
        string="Regulation Changes",
        comodel_name="ws_ra1505.regulation_business_environment",
        relation="rel_regulation_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "technology_business_environment_ids",
    )
    def _compute_technology_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.technology_business_environment_ids) > 0:
                result = True
            record.technology_business_environment_ok = result

    technology_business_environment_ok = fields.Boolean(
        string="Technology Advancement",
        compute="_compute_technology_business_environment_ok",
        store=True,
    )
    technology_business_environment_ids = fields.Many2many(
        string="Technology Advancements",
        comodel_name="ws_ra1505.technology_business_environment",
        relation="rel_technology_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "natural_business_environment_ids",
    )
    def _compute_natural_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.natural_business_environment_ids) > 0:
                result = True
            record.natural_business_environment_ok = result

    natural_business_environment_ok = fields.Boolean(
        string="Natural Cycle",
        compute="_compute_natural_business_environment_ok",
        store=True,
    )
    natural_business_environment_ids = fields.Many2many(
        string="Natural Cycles",
        comodel_name="ws_ra1505.natural_business_environment",
        relation="rel_natural_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )

    @api.depends(
        "energy_business_environment_ids",
    )
    def _compute_energy_business_environment_ok(self):
        for record in self:
            result = False
            if len(record.energy_business_environment_ids) > 0:
                result = True
            record.energy_business_environment_ok = result

    energy_business_environment_ok = fields.Boolean(
        string="Energy Availability & Cost",
        compute="_compute_energy_business_environment_ok",
        store=True,
    )
    energy_business_environment_ids = fields.Many2many(
        string="Energy Availability & Costs",
        comodel_name="ws_ra1505.energy_business_environment",
        relation="rel_energy_2_general_audit_standard_detail",
        column1="standard_detail_id",
        column2="business_environment_id",
    )
