# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import api, fields, models


class AccountantGeneralAuditStandardDetail(models.Model):
    _name = "accountant.general_audit_standard_detail"
    _inherit = "accountant.general_audit_standard_detail"

    business_process_id = fields.Many2one(
        string="Business Process",
        comodel_name="accountant.business_process",
        required=False,
        ondelete="restrict",
    )
    assersion_type_ids = fields.Many2many(
        string="Assersion Types",
        comodel_name="accountant.assersion_type",
        relation="rel_standard_detail_2_assersion_type",
        column1="standard_detail_id",
        column2="assersion_type_id",
    )

    rely_on_control = fields.Boolean(
        string="Rely on Control",
        default=False,
    )
    toc_analysis = fields.Selection(
        string="ToC Analysis",
        selection=[
            ("effective", "Effective"),
            ("not_effective", "Not Effective"),
            ("not_exist", "Not Exist"),
        ],
    )

    @api.depends(
        "rely_on_control",
        "toc_analysis",
    )
    def _compute_toc_result(self):
        for record in self:
            result = "high"
            if record.rely_on_control and record.toc_analysis == "effective":
                result = "low"
            record.toc_result = result

    toc_result = fields.Selection(
        string="ToC Result",
        selection=[
            ("low", "Low"),
            ("high", "High"),
        ],
        compute="_compute_toc_result",
        store=True,
    )
