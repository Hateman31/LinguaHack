import psycopg2
# from config import config_sql


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

def check_answer(conn_str, user_answer, quiz_id):
    sql = 'select 1 from speech_test where quiz_id=%s and answer=%s'
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql, [quiz_id, user_answer])
            # all_records = cursor.fetchall()
            # print('Connection was close')
            # return all_records
            if cursor.fetchall():
                return True
    return False

def get_speech_test(conn_str, quiz_id):
    sql = 'select question_text from speech_test where quiz_id=%s'
    with psycopg2.connect(conn_str) as conn:
        print('Connection is created')
        with conn.cursor() as cursor:
            cursor.execute(sql, [quiz_id])
            result = cursor.fetchone()
            print('Connection was close')
            return result[0]

if __name__ == '__main__':
    import config
    print(get_speech_test(config.conn_str, 1))