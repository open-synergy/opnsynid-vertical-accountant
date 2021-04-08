# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class AccountantClientTrialBalanceStandardDetail(models.Model):
    _name = "accountant.client_trial_balance_standard_detail"
    _description = "Accountant Client Trial Balance Standard Detail"
    _order = "sequence, trial_balance_id, id"
    _auto = False

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
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
            d.name AS name,
            d.code AS code,
            d.sequence AS sequence,
            COALESCE(e.previous_balance, 1.0) AS previous_balance,
            COALESCE(e.balance, 1.0) AS balance,
            a.id AS trial_balance_id
        """
        return select_str

    def _from(self):
        from_str = """
        accountant_client_trial_balance AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN accountant_client_account_type_set AS b ON
            a.account_type_set_id = b.id
        JOIN rel_accountant_type_set_2_account_type AS c ON
            b.id = c.account_client_type_set_id
        JOIN accountant_client_account_type AS d ON
            c.account_client_type_id = d.id
        RIGHT JOIN accountant_client_trial_balance_detail_summary AS e ON
            a.id = e.trial_balance_id AND
            d.id = e.type_id
        """
        return join_str

    def _group_by(self):
        group_str = """
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
