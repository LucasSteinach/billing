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
        SELECT id_client, balance, date_change, status FROM clients_table
        WHERE status = 'active'
    """
    pointer = connection.cursor()
    pointer.execute(balances_query)
    balances = pointer.fetchall()
    res = dict()
    for unit in balances:
        # unit[0] == id_client
        res[unit[0]] = {
                        'balance': float(unit[1]),
                        'date_change': str(unit[2]),
                        'status': unit[3],
                        }
    return res


def select_services(connection) -> dict:
    services_query = f"""
        SELECT r.id_relation, r.id_client, r.id_service, s.description, s.type, s.price 
        FROM relation_client_service_table r
        LEFT JOIN services_table s
        ON r.id_service = s.id_service
        WHERE s.status = 'active' AND r.status = 'active'
    """
    pointer = connection.cursor()
    pointer.execute(services_query)
    services = pointer.fetchall()
    res = dict()
    for service in services:
        # service[0] == id_relation
        res[service[0]] = {'id_client': service[1],
                           'id_service': service[2],
                           'description': service[3],
                           'type': service[4],
                           'price': float(service[5]),
                           }
    return res


def select_transactions(connection, status: str, filter: dict) -> dict:
    # fields in tarifficator_table:
    table_fields = {'id_transaction', 'id_relation', 'type', 'parameter', 'date', 'status'}
    if type(status) == str and status != '':
        if type(filter) == dict and set(filter.keys()).issubset(table_fields):
            conditions = ' AND '.join([f'{key} = {value}' for key, value in filter.items()])
            transactions_query = f"""
                SELECT id_transaction, id_relation, type, parameter, date_transaction
                FROM tarifficator_table
                WHERE status = '{status}' AND {conditions} 
            """
            pointer = connection.cursor()
            pointer.execute(transactions_query)
            transactions = pointer.fetchall()
            res = dict()
            for transaction in transactions:
                # transaction[0] == id_transaction
                res[transaction[0]] = {'id_relation': transaction[1],
                                       'type': transaction[2],
                                       'parameter': transaction[3],
                                       'date_transaction': str(transaction[4]),
                                      }
            return res


def insert_data(connection, table_name, col_data, values_data: str):

    if values_data != '' and type(col_data) == str:
        colum_data = ''
        if col_data != '':
            colum_data = f'({col_data})'
        insert_query = f"insert into {table_name} {colum_data} values ({values_data})"
        point = connection.cursor()
        point.execute(insert_query)
        connection.commit()
    return f'{len(values_data)} record(s) inserted into {table_name}'


def update_data(connection, table_name, condition_dict: dict, values_dict: dict):
    values = ', '.join(
        [
            f'{key} = {value}' if type(value) != str else f"{key} = '{value}'" for key, value in values_dict.items()
        ]
    )
    condition = ' AND '.join(
        [
            f'{key} = {value}' if type(value) != str else f"{key} = '{value}'" for key, value in condition_dict.items()
        ]
    )
    update_query = f"""UPDATE {table_name}
    SET {values}
    WHERE {condition};
    """
    pointer = connection.cursor()
    pointer.execute(update_query)
    connection.commit()
    return f'{table_name} updated'


def delete_data(connection, table_name, condition_dict: dict):
    if type(condition_dict) == dict:
        condition_length = sum([len(value) for value in condition_dict.values()])
        if condition_length != 0:
            conditions = ' AND '.join(
                [
                    f'{key} = {value}' if type(value) != str else
                    f"{key} = '{value}'" for key, value in condition_dict.items()
                ]
            )
            insert_query = f"delete from {table_name} where {conditions}"
            point = connection.cursor()
            point.execute(insert_query)
            connection.commit()
    return f'record(s) deleted from {table_name}'

def select_from_table(connection, table_name) -> list:
    select_query = f"""
        SELECT * FROM {table_name}
    """
    pointer = connection.cursor()
    pointer.execute(select_query)
    records = pointer.fetchall()
    return records
