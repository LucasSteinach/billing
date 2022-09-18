import os
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
from sql.sql_queries import sql_connection, select_transactions, select_from_table, select_services, insert_data
import sched
import time

s = sched.scheduler(time.time, time.sleep)


def connect_to_outer_service(id_service):
    return f'successful connection to service (id: {id_service})'


def tariffication(res):
    active_relations = select_services(conn)
    for id_relation, relation in active_relations.items():

        parameter = connect_to_outer_service(relation['id_service'])

        values = ', '.join(['DEFAULT',
                            str(id_relation),
                            f"'{relation['type']}'",

                            '1',  # parameter,

                            f"date '{str(datetime.now().date())}'",
                            "'not billed'"
                            ])
        insert_data(conn, 'tarifficator_table', values, '')

        res[id_relation] = 'succesfully inserted'

    return res


def main_execute(res):
    s.enter(3, 1, tariffication, argument=(res,))
    s.run()
    return res


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)

    tariffication_results = dict()

    print(main_execute(tariffication_results))
