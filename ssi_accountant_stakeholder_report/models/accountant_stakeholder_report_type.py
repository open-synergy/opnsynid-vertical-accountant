# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountantStakeholderReportType(models.Model):
    _name = "accountant_stakeholder_report_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Stakeholder Report Type"

    accountant_service_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Accountant Service Selection Method",
        required=True,
    )
    accountant_service_ids = fields.Many2many(
        comodel_name="accountant.service",
        string="Accountant Services",
        relation="rel_accountant_stakeholder_type_2_service",
    )
    accountant_service_domain = fields.Text(
        default="[]", string="Accountant Service Domain"
    )
    accountant_service_python_code = fields.Text(
        default="result = []", string="Accountant Service Python Code"
    )

    creditor_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Creditor Selection Method",
        required=True,
    )
    creditor_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Creditors",
        relation="rel_accountant_stakeholder_report_type_2_creditor",
    )
    creditor_domain = fields.Text(default="[]", string="Creditor Domain")
    creditor_python_code = fields.Text(
        default="result = []", string="Creditor Python Code"
    )
