# coding: utf8
from fundstrategy.core import sql_handler
from fundstrategy.core import models


class NavDao:
    def __init__(self, sql: sql_handler.SqlHandler):
        self.sql = sql

    def _row_to_nav(self, row: dict):
        return models.FundNav(date=row['value_date'],
                              value=row['unit_value'],
                              increase=row['increase_rate'])

    def insert_ignore(self, info: models.FundInfo, nav: models.FundNav):
        query = 'insert ignore into fund_nav(code,name,value_date,unit_value,increase_rate)' \
                ' values(%s,%s,%s,%s,%s)'
        args = (info.code, info.name, nav.date, nav.value, nav.increase)
        self.sql.do_insert(query, args)

    def get_nav(self, code: str, date: str) -> models.FundNav:
        query = 'select * from fund_nav where code=%s and value_date=%s'
        args = [code, date]
        row = self.sql.do_select(query, args, size=None)
        return self._row_to_nav(row)

    def list_navs(self, code: str, cond_sql: str = None, cond_args: list = None):
        query = 'select * from fund_nav where code=%s'
        args = [code]
        if cond_sql:
            query += f' and {cond_sql}'
            args += cond_args or []
        rows = self.sql.do_select(query, args, size=0)
        navs = [self._row_to_nav(r) for r in rows]
        return navs
