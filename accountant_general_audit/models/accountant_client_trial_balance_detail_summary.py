# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class AccountantClientTrialBalanceDetailSummary(models.Model):
    _name = "accountant.client_trial_balance_detail_summary"
    _description = "Accountant Client Trial Balance Detail Summary"
    _auto = False

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        required=True,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        required=True,
    )
    balance = fields.Float(
        string="Balance",
        required=True,
    )
    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.trial_balance_id AS trial_balance_id,
            a.type_id AS type_id,
            SUM(a.previous_balance) AS previous_balance,
            SUM(a.balance) AS balance
        """
        return select_str

    def _from(self):
        from_str = """
        accountant_client_trial_balance_detail AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    a.trial_balance_id,
                    a.type_id
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
