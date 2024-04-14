import psycopg2
from conn_preset import conn_str

schema_sql = open('schema.sql', encoding='utf-8').read()

def create_schema():
    with psycopg2.connect(conn_str) as db:
        with db.cursor() as cursor:
            cursor.execute(schema_sql)
            print('Schema created!')

if __name__ == '__main__':
    create_schema()