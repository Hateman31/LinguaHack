import psycopg2
import config as __cfg
from pathlib import Path

create_schema_sql = open('./schema.sql', encoding='utf-8').read() 


def create_schema():
    with psycopg2.connect(__cfg.config_sql) as db:
        with db.cursor() as cursor:
            cursor.execute(create_schema_sql)
            print('Schema created!')


def create_folders():
    audio_folder = Path.cwd() / 'audio'
    if not audio_folder.exists():
        audio_folder.mkdir()
    print('Folder for audio was created!')


def main():
    create_folders()
    create_schema()


if __name__ == '__main__':
    main()

