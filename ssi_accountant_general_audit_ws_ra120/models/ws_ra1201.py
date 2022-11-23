# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class WSAuditRA1201(models.Model):
    _name = "ws_ra1201"
    _description = "General Audit WS RA.120.1"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra120.worksheet_type_ra1201"

    account_mapping_ids = fields.One2many(
        string="Account Mappings",
        comodel_name="ws_ra1201.account_mapping",
        inverse_name="worksheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange("general_audit_id")
    def onchange_account_mapping_ids(self):
        self.update({"account_mapping_ids": [(5, 0, 0)]})
        Account = self.env["accountant.client_account"]
        if self.general_audit_id:
            result = []
            criteria = [("partner_id", "=", self.partner_id.id)]
            for account in Account.search(criteria):
                result.append(
                    (
                        0,
                        0,
                        {
                            "account_id": account.id,
                        },
                    )
                )
            self.update({"account_mapping_ids": result})

    @ssi_decorator.pre_confirm_check()
    def _check_mapping(self):
        for mapping in self.account_mapping_ids:
            if not mapping.type_id:
                error_message = """
                Context: Confirming WS.120.1
                Database ID: %s
                Problem: Not all account mapped to standard account
                Solution: Map all account to standard account
                """ % (
                    self.id
                )
                raise ValidationError(_(error_message))
