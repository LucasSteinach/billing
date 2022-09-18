import os

from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, select_balances, select_from_table, select_services, \
    select_transactions, update_data
import sched
import time

s = sched.scheduler(time.time, time.sleep)


def daily_billing(connection):
    pass


def billing_execute(connection, transactions_dict, balances_dict):
    s.enter(20, 1, daily_billing, argument=(connection, transactions_dict, balances_dict))
    s.run()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)

    active_relations = select_services(conn)
    print('active_relations', '\n', active_relations, '\n', '------')
    clients_list = select_balances(conn)
    print('clients_list', '\n', clients_list, '\n', '------')

    # print('select_transactions', '\n', select_transactions(conn, 'not billed', {'id_relation': 2}))
    for id_relation, relation in active_relations.items():
        transactions_related = select_transactions(conn, 'not billed', {'id_relation': id_relation})
        # alter transaction_status to 'pending'
        print('id_relation', id_relation, '\n', transactions_related)
        sum_to_write_off = sum(
            [
                active_relations[transaction['id_relation']]['price']
                for id_transaction, transaction
                in transactions_related.items()
            ]
        )
        # insert transaction into billing with status 'processing'

    #     try except this block
        buffer = update_data(conn,
                             'clients_table',
                             {'id_client': relation['id_client']},
                             {'balance': clients_list[relation['id_client']]['balance'] - sum_to_write_off}
                             )
        print(buffer)
    #    /try except this block

    # billing_execute(conn)
