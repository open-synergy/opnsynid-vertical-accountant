# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import models


class WSAuditRA1102(models.Model):
    _name = "ws_rr1102"
    _description = "General Audit WS RA.110.2"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_rr110.worksheet_type_rr1102"
