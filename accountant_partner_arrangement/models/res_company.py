# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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

    @api.model
    def _get_partner_arrangement_button_policy_map(self):
        return [
            ("confirm_ok",
                "accountant_partner_arrangement_confirm_grp_ids"),
            ("valid_ok", "accountant_partner_arrangement_valid_grp_ids"),
            ("cancel_ok", "accountant_partner_arrangement_cancel_grp_ids"),
            ("restart_ok", "accountant_partner_arrangement_restart_grp_ids"),
        ]

    @api.multi
    def _get_partner_arrangement_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids += getattr(
            self, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result
