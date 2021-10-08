# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditRelatedParty(models.Model):
    _name = "accountant.general_audit_related_party"
    _description = "Accountant General Audit Related Party"

    index_a2303_id = fields.Many2one(
        string="Index A.230.3",
        comodel_name="accountant.general_audit_index_a2303",
        ondelete="cascade",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        # related="general_audit_id.partner_id",
        required=True,
        ondelete="restrict",
    )
    relationship_type_id = fields.Many2one(
        string="Relationship Type",
        comodel_name="res.partner.related_party_relationship_type",
        # related="general_audit_id.partner_id",
        # res.partner.related_party_relationship_type,
        required=True,
        ondelete="restrict",
    )
    transaction_type_id = fields.Many2one(
        string="Transcation Type",
        comodel_name="res.partner.related_party_transaction_type",
        # related="general_audit_id.partner_id",
        # res.partner.related_party_transaction_type,
        required=True,
        ondelete="restrict",
    )
