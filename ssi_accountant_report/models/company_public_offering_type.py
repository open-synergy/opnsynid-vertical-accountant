# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class CompanyPublicOfferingType(models.Model):
    _inherit = "company_public_offering_type"

    p2pk_go_public = fields.Boolean(
        string="Go Public",
    )
