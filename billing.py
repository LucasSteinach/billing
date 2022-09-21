import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, select_balances, select_services, \
    select_transactions, update_data, insert_data, delete_data
import sched
import time

s = sched.scheduler(time.time, time.sleep)


# def daily_billing(connection):
#     pass


# def billing_execute(connection, transactions_dict, balances_dict):
#     s.enter(20, 1, daily_billing, argument=(connection, transactions_dict, balances_dict))
#     s.run()


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

        update_data(conn, 'tarifficator_table',
                    condition_dict={'id_relation': id_relation, },
                    values_dict={'status': 'processing', }
                    )
        print('id_relation', id_relation, '\n', transactions_related)
        sum_to_write_off = 0
        for id_transaction, transaction in transactions_related.items():
            values_data = ', '.join([
                'DEFAULT',
                str(id_transaction),
                str(relation['id_client']),
                str(relation['id_service']),
                str(relation['price']),
                f"date '{datetime.now().date()}'",
                "'processing'",
            ])
            insert_data(conn, 'billing_table', '', values_data)
            sum_to_write_off += relation['price']

        try:
            update_data(
                conn,
                'clients_table',
                {'id_client': relation['id_client']},
                {'balance': clients_list[relation['id_client']]['balance'] - sum_to_write_off}
                )
            update_data(
                conn,
                'tarifficator_table',
                condition_dict={
                    'status': "processing",
                    'id_relation': id_relation,
                },
                values_dict={
                    'status': 'DONE'
                }
            )
            update_data(
                conn,
                'billing_table',
                condition_dict={
                    'status': "processing",
                    'id_client': relation['id_client'],
                },
                values_dict={
                    'status': 'DONE'
                }
            )

        except psycopg2.OperationalError as error:
            print(f'Error {error} occured')
            update_data(
                conn,
                'tarifficator_table',
                condition_dict={
                    'status': 'processing',
                    'id_relation': id_relation,
                },
                values_dict={
                    'status': 'not billed'
                }
            )
            delete_data(
                conn,
                'billing_table',
                condition_dict={
                    'status': 'processing',
                    'id_client': relation['id_client'],
                }
            )

    # billing_execute(conn)
