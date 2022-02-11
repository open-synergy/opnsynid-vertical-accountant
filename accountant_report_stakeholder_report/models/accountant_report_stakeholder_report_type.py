# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantReportStakeholderReportType(models.Model):
    _name = "accountant.report_stakeholder_report_type"
    _description = "Accounting Report Stakeholder Report Type"

    name = fields.Char(
        string="Name",
        required=True,
    )

    code = fields.Char(
        string="Code",
        required=True,
    )

    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        ondelete="restrict",
    )

    domain = fields.Text(string="Domain", required=True, default="[]")

    confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm",
        comodel_name="res.groups",
        relation="rel_stakeholder_report_type_confirm_group",
        column1="type_id",
        column2="group_id",
    )

    cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel",
        comodel_name="res.groups",
        relation="rel_stakeholder_report_type_cancel_group",
        column1="type_id",
        column2="group_id",
    )

    restart_grp_ids = fields.Many2many(
        string="Allowed To Restart",
        comodel_name="res.groups",
        relation="rel_stakeholder_report_type_restart_group",
        column1="type_id",
        column2="group_id",
    )

    restart_validation_grp_ids = fields.Many2many(
        string="Allowed To Restart Validation",
        comodel_name="res.groups",
        relation="rel_stakeholder_report_type_restart_validation_group",
        column1="type_id",
        column2="group_id",
    )
