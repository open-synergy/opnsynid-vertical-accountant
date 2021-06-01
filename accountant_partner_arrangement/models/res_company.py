# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Accountant Config
    accountant_partner_arrangement_sequence_id = fields.Many2one(
        string="Accountant Firm Partner Arrangement Sequence",
        comodel_name="ir.sequence",
    )
    accountant_partner_arrangement_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Accountant Firm Partner Arrangement",
        comodel_name="res.groups",
        relation="rel_accountant_partner_arrangement_allowed_confirm_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_partner_arrangement_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Accountant Firm Partner Arrangement",
        comodel_name="res.groups",
        relation="rel_accountant_partner_arrangement_allowed_valid_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_partner_arrangement_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Accountant Firm Partner Arrangement",
        comodel_name="res.groups",
        relation="rel_accountant_partner_arrangement_allowed_cancel_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_partner_arrangement_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Accountant Firm Partner Arrangement",
        comodel_name="res.groups",
        relation="rel_accountant_partner_arrangement_allowed_restart_groups",
        column1="company_id",
        column2="group_id",
    )
    accountant_partner_arrangement_restart_approval_grp_ids = fields.Many2many(
        string="Allowed To Restart Approval Accountant Firm Partner Arrangement",
        comodel_name="res.groups",
        relation="rel_partner_arrangement_restart_approval_groups",
        column1="company_id",
        column2="group_id",
    )
