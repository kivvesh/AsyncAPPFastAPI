import json
from elasticsearch import helpers


def create_index_filmwork(client):
    with open('settings_movie.json', 'r') as file:
        settings = json.load(file)
    with open('mappings_movie.json', 'r') as file:
        mappings = json.load(file)
    try:
        get = client.indices.get(index='movies')
    except Exception as error:
        client.indices.create(
            index='movies',
            mappings=mappings,
            settings=settings
        )
    return client


def create_index_person(client):
    with open('settings_person.json', 'r') as file:
        settings = json.load(file)
    with open('mappings_person.json', 'r') as file:
        mappings = json.load(file)
    try:
        get = client.indices.get(index='persons')
    except Exception as error:
        client.indices.create(
            index='persons',
            mappings=mappings,
            settings=settings
        )
    return client


def create_index_genre(client):
    with open('settings_genre.json', 'r') as file:
        settings = json.load(file)
    with open('mappings_genre.json', 'r') as file:
        mappings = json.load(file)
    try:
        get = client.indices.get(index='genres')
    except Exception as error:
        client.indices.create(
            index='genres',
            mappings=mappings,
            settings=settings
        )
    return client


def generate_docs_films(list_films):
    for film in list_films.values():
        film["_index"] = "movies"
        film["_id"] = film["id"]
        yield film


def generate_docs_persons(list_films):
    for film in list_films.values():
        film["_index"] = "persons"
        film["_id"] = film["id"]
        yield film


def generate_docs_genres(list_genres):
    for genre in list_genres.values():
        genre["_index"] = "genres"
        genre["_id"] = genre["id"]
        yield genre


def add_documents(list_films, client):  # загрузка фильмов в elasticsearch
    client = create_index_filmwork(client)
    helpers.bulk(client, generate_docs_films(list_films))


def add_person_documents(list_person, client):
    client = create_index_person(client)
    helpers.bulk(client, generate_docs_persons(list_person))


def add_genre_documents(list_genre, client):
    client = create_index_genre(client)
    helpers.bulk(client, generate_docs_genres(list_genre))
