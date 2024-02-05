# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantService(models.Model):
    _name = "accountant.service"
    _inherit = [
        "accountant.service",
        "mixin.res_partner_m2o_configurator",
    ]
    _res_partner_m2o_configurator_insert_form_element_ok = True
    _res_partner_m2o_configurator_form_xpath = "//page[@name='partner']"

    partner_ids = fields.Many2many(
        relation="rel_accountant_service_2_partner",
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
        relation="rel_accountant_service_2_creditor",
    )
    creditor_domain = fields.Text(default="[]", string="Creditor Domain")
    creditor_python_code = fields.Text(
        default="result = []", string="Creditor Python Code"
    )

    accountant_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Accountant Selection Method",
        required=True,
    )
    accountant_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Accountants",
        relation="rel_accountant_service_2_accountant",
    )
    accountant_domain = fields.Text(default="[]", string="Accountant Domain")
    accountant_python_code = fields.Text(
        default="result = []", string="Accountant Python Code"
    )
