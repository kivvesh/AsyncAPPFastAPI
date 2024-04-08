import logging
import time

import psycopg2
from psycopg2.extras import DictCursor
from elasticsearch import Elasticsearch

from modules.backoff import backoff
from modules.extract_data_from_psql import extract_data_from_psql
from config import settings


@backoff()
def connect_psql_elastic():
    """Проверяет доступность соединения с Elasticsearch и PostgreSQL"""

    try:
        client = Elasticsearch(
            f'http://{settings.elastic_host}:{settings.elastic_port}/'
        )

        connection = psycopg2.connect(
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            options=settings.postgres_options,
            cursor_factory=DictCursor
        )

        cursor = connection.cursor()
        extract_data_from_psql(cursor, client)
    except Exception as error:
        logging.error(error)
    finally:
        connection.close()
        client.close()


if __name__ == '__main__':
    while True:
        connect_psql_elastic()
        time.sleep(5)
