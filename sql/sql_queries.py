import psycopg2
from models.models import Balance, Transaction


def sql_connection(db_name: str,
                   db_user: str,
                   db_password: str,
                   db_host: str,
                   db_port: str,
                   target_session_attrs: str,
                   sslmode: str):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            target_session_attrs=target_session_attrs,
            sslmode=sslmode
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as error:
        print(f"The error '{error}' occurred")
    return connection


def select_balances(connection) -> dict:
    balances_query = f"""
        SELECT id_client, current_balance, last_changing, status FROM balance
    """
    pointer = connection.cursor()
    pointer.execute(balances_query)
    balances = pointer.fetchall()
    res = dict()
    for unit in balances:
        res[unit[0]] = Balance(*unit)
    return res


def select_services(connection) -> dict:
    services_query = f"""
        SELECT r.id, s.price 
        FROM relation_client_service r
        LEFT JOIN services s
        ON r.id_service = s.id
        WHERE s.status = 'Active' AND r.status = 'Active'
    """
    pointer = connection.cursor()
    pointer.execute(services_query)
    services = pointer.fetchall()
    res = dict()
    for service in services:
        res[service[0]] = service[1]
    return res


def select_transactions(connection) -> dict:
    transactions_query = f"""
        SELECT t.id_relation, r.id_client t.action_type, t.parameter, t.date, COUNT(t.id_relation)
        FROM tarificator as t
        LEFT JOIN relation_client_service r
        GROUP BY t.id_relation
    """
    pointer = connection.cursor()
    pointer.execute(transactions_query)
    transactions = pointer.fetchall()
    res = dict()
    for transaction in transactions:
        res[transaction[0]] = Transaction(*transaction)
    return res


def insert_data(connection, table_name, colum_data, values_data):
    if values_data != '':
        insert_query = f"insert into {table_name} ({colum_data}) values ({values_data})"
        point = connection.cursor()
        point.execute(insert_query)
        connection.commit()


def alter_data(connection, table_name, values_data, colum_data='', ):
    pass


def select_from_table(connection, table_name) -> list:
    select_query = f"""
        SELECT * FROM {table_name}
    """
    pointer = connection.cursor()
    pointer.execute(select_query)
    records = pointer.fetchall()
    return records
