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


def select_initial(connection):
    clients_query = f"""
        SELECT id FROM clients
    """
    pointer = connection.cursor()
    pointer.execute(clients_query)
    clients = pointer.fetchall()

    balances_query = f"""
        SELECT id_client, current_balance, last_changing, status FROM balance
    """
    pointer = connection.cursor()
    pointer.execute(balances_query)
    balances = pointer.fetchall()

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
    return clients, balances, transactions


def select_from_table(connection, table_name) -> list:
    select_query = f"""
        SELECT * FROM {table_name}
    """
    pointer = connection.cursor()
    pointer.execute(select_query)
    records = pointer.fetchall()
    return records
