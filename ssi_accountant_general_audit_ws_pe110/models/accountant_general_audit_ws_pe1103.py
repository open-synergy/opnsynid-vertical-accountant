# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import models


class AccountantGeneralWSAuditPE1103(models.Model):
    _name = "accountant.general_audit_ws_pe1103"
    _description = "General Audit WS PE.1103"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_pe110.worksheet_type_pe1103"