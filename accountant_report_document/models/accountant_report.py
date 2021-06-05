# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    attachment_ids = fields.One2many(
        string="Attachments",
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[
            ("res_model", "=", "accountant.report"),
        ],
        auto_join=True,
    )
    main_report_attachment_id = fields.Many2one(
        string="Main Report Attachment",
        comodel_name="ir.attachment",
        readonly=True,
        states={
            "finalize": [
                ("readonly", False),
            ],
        },
    )
    draft_report_attachment_id = fields.Many2one(
        string="Draft Report Attachment",
        comodel_name="ir.attachment",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
