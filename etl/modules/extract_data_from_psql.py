import logging
import time

from modules.load import add_documents, add_person_documents, \
    add_genre_documents
from modules.state_storage import JsonFileStorage, State
from modules.transform import Filmwork, Person, Genre, return_json_films, \
    return_json_persons, return_json_genres


def load_person_film_work(persons_values, cursor):
    persons_id = [i[0] for i in persons_values]
    query2 = f'''
                    SELECT fw.id, fw.modified
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    WHERE pfw.person_id IN {tuple(persons_id)}
                    ORDER BY fw.modified; 
                '''
    cursor.execute(query2)
    return cursor.fetchall()


def load_genre_film_work(genres_values, cursor):
    genres_id = [i[0] for i in genres_values]
    query2 = f'''
                        SELECT fw.id, fw.modified
                        FROM content.film_work fw
                        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                        WHERE gfw.genre_id IN {tuple(genres_id)}
                        ORDER BY fw.modified;
                    '''
    cursor.execute(query2)
    return cursor.fetchall()


def load_film_work(film_work_list, cursor):
    films_id = [i[0] for i in film_work_list]
    query3 = f'''
                    SELECT
                        fw.id, 
                        fw.title, 
                        fw.description, 
                        fw.rating, 
                        fw.type, 
                        fw.created, 
                        fw.modified as modified, 
                        pfw.role, 
                        p.id,
                        p.full_name,
                        g.name
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN content.person p ON p.id = pfw.person_id
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    WHERE fw.id IN {tuple(films_id)}; 
                '''

    cursor.execute(query3)
    films = cursor.fetchall()
    return films


def extract_data_from_psql(cursor, client):
    state = State(JsonFileStorage('config.json'))

    query_person = f'''
        select id, full_name, created, modified from person
        where modified > '{state.get_state('MODIFIED_PERSONS')}'
        order by modified
        limit {state.get_state('LIMIT_PERSONS')}
'''
    cursor.execute(query_person)
    persons = cursor.fetchall()
    if len(persons) != 0:
        persons_json = return_json_persons(persons)
        valid_persons_json = {}
        for key in persons_json.keys():
            try:
                valid_persons_json[key] = dict(Person(**(persons_json[key])))
            except Exception as error:
                logging.error(error)
        try:
            add_person_documents(valid_persons_json, client)
            state.set_state('MODIFIED_PERSONS', str(persons[-1][-1]))
        except Exception as error:
            logging.error(error)

    query_genre = f'''
            select id, name, description, created, modified from genre
            where modified > '{state.get_state('MODIFIED_GENRES')}'
            order by modified
            limit {state.get_state('LIMIT_GENRES')}
    '''
    cursor.execute(query_genre)
    genres = cursor.fetchall()
    if len(genres) != 0:
        genres_json = return_json_genres(genres)
        valid_genres_json = {}
        for key in genres_json.keys():
            try:
                valid_genres_json[key] = dict(Genre(**(genres_json[key])))
            except Exception as error:
                logging.error(error)
        try:
            add_genre_documents(valid_genres_json, client)
            state.set_state('MODIFIED_GENRES', str(genres[-1][-1]))
        except Exception as error:
            logging.error(error)

    query1 = f'''
                select id,modified from person
                where modified > '{state.get_state('MODIFIED_PERSON')}'
                order by modified
                limit {state.get_state('LIMIT_PERSON')}
            '''
    cursor.execute(query1)
    persons_values = cursor.fetchall()

    if len(persons_values) != 0:
        persons_film_work_list = load_person_film_work(persons_values, cursor)
        films = load_film_work(persons_film_work_list, cursor)
        films_person_json = return_json_films(films)  # вовзращаем список фильмов по измененых person
        valid_json_film1 = {}
        for j in films_person_json.keys():
            try:
                valid_json_film1[j] = dict(Filmwork(**(films_person_json[j])))  # проверка на валидность данных
            except Exception as error:
                logging.error(error)

        try:
            add_documents(valid_json_film1, client)
            state.set_state('MODIFIED_PERSON', str(persons_values[-1][1]))
        except Exception as error:
            logging.error(error)

    query2 = f'''
                        select id,modified from genre
                        where modified > '{state.get_state('MODIFIED_GENRE')}' 
                        order by modified 
                        limit {state.get_state('LIMIT_GENRE')}
                    '''
    cursor.execute(query2)
    genres_values = cursor.fetchall()

    if len(genres_values) != 0:
        genres_film_work_list = load_genre_film_work(genres_values, cursor)
        films = load_film_work(genres_film_work_list, cursor)
        films_genre_json = return_json_films(films)
        valid_json_film2 = {}

        for j in films_genre_json.keys():
            try:
                valid_json_film2[j] = dict(Filmwork(**(films_genre_json[j])))  # проверка на валидность данных
            except Exception as error:
                logging.error(error)
        try:
            time.sleep(10)
            add_documents(valid_json_film2, client)
            # запись в .env MODIFIED_PERSON
            state.set_state('MODIFIED_GENRE',str(persons_values[-1][1]))
        except Exception as error:
            logging.error(error)

    query3 = f'''
                                select id,modified from film_work
                                where modified > '{state.get_state('MODIFIED_FILMWORK')}'
                                order by modified
                                limit {state.get_state('LIMIT_FILMWORK')}
                            '''
    cursor.execute(query3)
    films_values = cursor.fetchall()
    if len(films_values) != 0:
        films = load_film_work(films_values, cursor)
        films_json = return_json_films(films)
        valid_json_film3 = {}

        for j in films_json.keys():
            try:
                valid_json_film3[j] = dict(Filmwork(**(films_json[j])))  # проверка на валидность данных
            except Exception as error:
                logging.error(error)
        try:
            time.sleep(10)
            add_documents(valid_json_film3, client)
            state.set_state('MODIFIED_FILMWORK',str(persons_values[-1][1]))
        except Exception as error:
            logging.error(error)
