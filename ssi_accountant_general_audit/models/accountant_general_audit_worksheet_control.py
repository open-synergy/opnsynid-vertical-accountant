# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models, tools


class AccountantGeneralAuditWorksheetControl(models.Model):
    _name = "accountant.general_audit_worksheet_control"
    _description = "Accountant General Audit Worksheet Control"
    _auto = False
    _order = "general_audit_id, type_id"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.general_audit_worksheet_type",
        required=False,
    )

    def _compute_worksheet_id(self):
        for record in self:
            result = False
            worksheets = record.general_audit_id.worksheet_ids.filtered(
                lambda r: r.parent_type_id.id == record.type_id.id
            )
            if len(worksheets) > 0:
                result = worksheets[0]
            record.worksheet_id = result

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="accountant.general_audit_worksheet",
        compute="_compute_worksheet_id",
        store=False,
    )
    required = fields.Boolean(
        string="Required",
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        related="worksheet_id.user_id",
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="accountant.general_audit_worksheet_conclusion",
        related="worksheet_id.conclusion_id",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        related="worksheet_id.state",
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            SELECT
                row_number() OVER() as id,
                a.general_audit_id,
                a.type_id,
                a.required
            FROM (
            SELECT general_audit_id, type_id, required
            FROM accountant_general_audit_worksheet_control_required
            UNION
            SELECT general_audit_id, type_id, required
            FROM accountant_general_audit_worksheet_control_additional
            ) AS a
        )"""
            % (self._table,)
        )
