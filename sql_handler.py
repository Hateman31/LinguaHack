import psycopg2
from connection_str import config_sql


def check_quiz_id(conn_str, sql, user_id):
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql, [user_id])
            all_records = cursor.fetchone()
            print('Connection was close')
    return all_records


def get_info(conn_str, sql, extension_str):
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql, [extension_str])
            all_records = cursor.fetchall()
            print('Connection was close')
    return all_records


def get_available_quest(conn_str, sql, user_id, quiz_id):
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql, [user_id, quiz_id])
            all_records = cursor.fetchall()
            print('Connection was close')
    return all_records


def editing_info(conn_str, sql, *extension_str):
    with psycopg2.connect(conn_str) as conn:
        print('Record is started')
        with conn.cursor() as cursor:
            cursor.execute(sql, extension_str)
            print('Record if finished')
