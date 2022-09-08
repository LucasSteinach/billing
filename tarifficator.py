import os
from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, select_transactions
from models.models import Transaction
import sched
import time


s = sched.scheduler(time.time, time.sleep)


def main_execute(res):
    s.enter(20, 1, daily_download, res)
    s.run()
    return res


def daily_download(res):
    transactions = select_transactions(conn)
    for data_unit in transactions:
        tr_act_unit = Transaction(*data_unit)
        res.append(tr_act_unit)
    return res


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)
    transactions_list = []
    result_sheduled = main_execute(transactions_list)
