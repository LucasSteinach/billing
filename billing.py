import os
from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, alter_data
import sched
import time

s = sched.scheduler(time.time, time.sleep)


#  transactions_list - list of Transaction-objects from tarifficator.py
#  balances_dict - dict of Balance-objects from main.py
def daily_billing(connection, transactions_list, balances_dict):
    values = []
    for unit in transactions_list:
        if unit.client_id in balances_dict.keys():
            balances_dict[unit.client_id].calculate(unit)
            values.append(*balances_dict[unit.client_id])
    alter_data(connection, 'balance', ','.join(values))


def billing_execute(connection, transactions_list, balances_dict):
    s.enter(20, 1, daily_billing, argument=(connection, transactions_list, balances_dict))
    s.run()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)

    # billing_execute(conn, transactions_list, balances_dict)
