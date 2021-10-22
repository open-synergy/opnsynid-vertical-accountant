# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import csv
from tempfile import TemporaryFile

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ImportTrialBalanceDetail(models.TransientModel):
    _name = "accountant.import_trial_balance_detail"
    _description = "Import Trial Balance Detail"

    @api.model
    def _default_trial_balance_id(self):
        return self.env.context.get("active_id", False)

    trial_balance_id = fields.Many2one(
        string="# Trial Balance",
        comodel_name="accountant.client_trial_balance",
        default=lambda self: self._default_trial_balance_id(),
        store=True,
        compute=False,
    )
    data = fields.Binary(string="File", required=True)

    @api.multi
    def button_import(self):
        self.ensure_one()
        fileobj = TemporaryFile("w+")
        fileobj.write(base64.decodestring(self.data))
        fileobj.seek(0)
        reader = csv.reader(fileobj, delimiter=",")
        self.trial_balance_id.detail_ids.unlink()
        for row in reader:
            self._create_trial_balance_detail(row)

        fileobj.close()
        return {"type": "ir.actions.act_window_close"}

    @api.multi
    def _create_trial_balance_detail(self, row):
        self.ensure_one()
        obj_detail = self.env["accountant.client_trial_balance_detail"]
        obj_detail.create(self._prepare_trial_balance_detail(row))

    @api.multi
    def _prepare_trial_balance_detail(self, row):
        self.ensure_one()
        account = self._get_account(row[1])

        return {
            "trial_balance_id": self.trial_balance_id.id,
            "account_id": account.id,
            "balance": row[3],
            "interim_balance": row[4],
            "previous_balance": row[5],
        }

    @api.multi
    def _get_account(self, code):
        self.ensure_one()
        obj_account = self.env["accountant.client_account"]
        partner = self.trial_balance_id.partner_id
        criteria = [
            ("code", "=", code),
            ("partner_id.id", "=", partner.id),
        ]
        accounts = obj_account.search(criteria)
        if len(accounts) > 0:
            result = accounts[0]
        else:
            error_message = _("Invalid client account")
            raise UserError(error_message)
        return result
