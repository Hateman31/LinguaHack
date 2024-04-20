import psycopg2
import config as __cfg
from pathlib import Path

create_schema_sql = open('sql/schema.sql', encoding='utf-8').read()
fill_tables_sql = open('sql/insert_tables.sql', encoding='utf-8').read()


def create_schema():
    with psycopg2.connect(__cfg.conn_str) as db:
        with db.cursor() as cursor:
            cursor.execute(create_schema_sql)
            print('Schema created!')


def create_folders():
    audio_folder = Path.cwd() / 'audio'
    if not audio_folder.exists():
        audio_folder.mkdir()
    print('Folder for audio was created!')


def fill_the_tables():
    with psycopg2.connect(__cfg.conn_str) as conn:
        print('Record is started')
        with conn.cursor() as cursor:
            cursor.execute(fill_tables_sql)
            print('Record if finished')


def main():
    create_folders()
    create_schema()
    fill_the_tables()


if __name__ == '__main__':
    main()

