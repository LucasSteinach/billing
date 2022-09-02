import os
from sql.sql_queries import sql_connection, select_initial
from dotenv import load_dotenv, find_dotenv

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    sql_my_auth_data = tuple(os.getenv('sql_my_auth_data').split(','))
    conn = sql_connection(*sql_my_auth_data)
    clients_list, balances_list, transactions_list = select_initial(conn)
