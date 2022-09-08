import psycopg2


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


def select_balances(connection):
    balances_query = f"""
        SELECT id_client, current_balance, last_changing, status FROM balance
    """
    pointer = connection.cursor()
    pointer.execute(balances_query)
    balances = pointer.fetchall()
    res = dict()
    for unit in balances:
        res[unit[0]] = unit
    return res


def select_transactions(connection):
    transactions_query = f"""
        SELECT t.id, c.id, s.id, t.action_type, t.parameter, t.date
        FROM tarificator as t
        LEFT JOIN relation_client_service as r
        ON t.id_relation = r.id
        LEFT JOIN clients as c
        ON r.id_client = c.id
        LEFT JOIN services as s
        ON r.id_service = s.id
    """
    pointer = connection.cursor()
    pointer.execute(transactions_query)
    transactions = pointer.fetchall()
    return transactions


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
