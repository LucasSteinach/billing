import os
from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, alter_data, select_balances, select_from_table, select_services
import sched
import time

s = sched.scheduler(time.time, time.sleep)


#  transactions_dict - dict {relation_id: Transaction} from tarifficator.py
#  balance_dict - dict {id_client: Balance} from main.py
def daily_billing(connection, transactions_dict, balance_dict):
    balance_dict = select_balances(conn)
    service_prices = select_services(conn)
    for relation_id, transaction in transactions_dict.items():
        withdrawn = transaction.count * service_prices[relation_id]
        balance_dict[transaction.id_client].calculate(withdrawn)
    print (f"{len(transactions_dict)} write-offs completed")


        # balance_dict[transaction.id_client].calculate()


def billing_execute(connection, transactions_dict, balances_dict):
    s.enter(20, 1, daily_billing, argument=(connection, transactions_dict, balances_dict))
    s.run()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)



    # billing_execute(conn, transactions_list, balances_dict)
