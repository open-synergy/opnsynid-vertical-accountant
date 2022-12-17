# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _inherit = "accountant.general_audit_standard_detail"

    pr_assersion_type_ids = fields.Many2many(
        string="Assersion Types on Presentation and Disclosure",
        comodel_name="accountant.assersion_type",
        relation="rel_standard_detail_2_pr_assersion_type",
        column1="standard_detail_id",
        column2="assersion_type_id",
    )
    romm = fields.Selection(
        string="Risk Material Misstatement",
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
    )
    planned_response_analytic_procedure = fields.Boolean(
        string="Planned Response Analytic Procedure",
        default=False,
    )
    planned_response_tod = fields.Boolean(
        string="Planned Response ToD",
        default=False,
    )
    planned_response_interim = fields.Boolean(
        string="Planned Response on Interim",
        default=False,
    )
    planned_response_ye = fields.Boolean(
        string="Planned Response on Year End",
        default=False,
    )
