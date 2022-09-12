import os
from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, select_transactions, select_from_table, select_services
from models.models import Transaction
import sched
import time


s = sched.scheduler(time.time, time.sleep)


def main_execute(res):
    s.enter(20, 1, daily_download, res)
    s.run()
    return res


def daily_download(res):
    # get transaction for every active relation with its quantity  (res = {relation_id: Transaction)
    res = select_transactions(conn)
    return res


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)

    tariff_res = None
    main_execute(tariff_res)
