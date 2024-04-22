import psycopg2
import config as __cfg
from pathlib import Path

create_schema_sql = open('sql/schema.sql', encoding='utf-8').read()
fill_tables_sql = open('sql/insert_tables.sql', encoding='utf-8').read()


def schema_completed():
    sql = '''
        SELECT count(1) = 5
        FROM information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name  in ('quizzes', 'options', 'user_answers', 'users', 'speech_test')'''
    with psycopg2.connect(__cfg.conn_str) as db:
        with db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]

def create_schema():
    with psycopg2.connect(__cfg.conn_str) as db:
        with db.cursor() as cursor:
            cursor.execute(create_schema_sql)
            print('Schema created!')


def create_folder(folder_name):
    folder = Path.cwd() / folder_name
    if not folder.exists():
        folder.mkdir()
        print(f'Folder for {folder} was created!')


def fill_the_tables():
    with psycopg2.connect(__cfg.conn_str) as conn:
        print('Record is started')
        with conn.cursor() as cursor:
            cursor.execute(fill_tables_sql)
            print('Record if finished')


def main():
    for f in ['audio', 'media']:
        create_folder(f)
    if not schema_completed():
        create_schema()
        fill_the_tables()

if __name__ == '__main__':
    main()

