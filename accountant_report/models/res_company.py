# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Accountant Config
    accountant_report_sequence_id = fields.Many2one(
        string="Accountant Report Sequence",
        comodel_name="ir.sequence",
    )
    accountant_report_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Accountant Report",
        comodel_name="res.groups",
        relation="rel_accountant_report_allowed_confirm_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_report_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Accountant Report",
        comodel_name="res.groups",
        relation="rel_accountant_report_allowed_valid_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_report_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Accountant Report",
        comodel_name="res.groups",
        relation="rel_accountant_report_allowed_cancel_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_report_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Accountant Report",
        comodel_name="res.groups",
        relation="rel_accountant_report_allowed_restart_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_report_finalize_grp_ids = fields.Many2many(
        string="Allowed To Finalize Accountant Report",
        comodel_name="res.groups",
        relation="rel_accountant_report_allowed_finalize_groups",
        column1="company_id",
        column2="group_id",
    )
