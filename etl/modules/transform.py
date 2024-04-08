import datetime
import uuid
from typing import Any, Union

from pydantic import BaseModel


class Filmwork(BaseModel):
    id: str
    title: str
    description: str | None
    imdb_rating: float | Any
    actors: list[dict | None]
    actors_names: list[str | None]
    directors: list[dict | None]
    directors_names: list[str | None]
    writers: list[dict | None]
    writers_names: list[str | None]
    genre: list[str | None]


class Genre(BaseModel):
    id: str
    name: str
    description: str | None
    created: datetime.datetime
    modified: datetime.datetime

class Person(BaseModel):
    id: str
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime



def return_json_persons(persons):#преобразование данных persons в json
    persons_json = {}
    for person in persons:
        if person[0] not in persons_json:
            persons_json[person[0]] = {
                'id': person[0],
                'full_name': person[1],
                'created': person[2],
                'modified': person[3],
            }
    return persons_json


def return_json_genres(genres):#преобразование данных genre в json
    genres_json = {}
    for genre in genres:
        if genre[0] not in genres_json:
            genres_json[genre[0]] = {
                'id': genre[0],
                'name': genre[1],
                'description': genre[2],
                'created': genre[3],
                'modified': genre[4],
            }
    return genres_json


def return_json_films(films):
    films_json = {}
    for film in films:
        if film[0] not in films_json:
            films_json[film[0]] = {
                'id': film[0],
                'title': film[1],
                'description': film[2],
                'imdb_rating': film[3],
            }
            if film[7] == 'actor':
                films_json[film[0]]['actors'] = [{'id': film[8],'name': film[9]}]
                films_json[film[0]]['actors_names'] = [film[9]]
                films_json[film[0]]['directors'] = []
                films_json[film[0]]['directors_names'] = []
                films_json[film[0]]['writers'] = []
                films_json[film[0]]['writers_names'] = []

            elif film[7] == 'director':
                films_json[film[0]]['actors'] = []
                films_json[film[0]]['actors_names'] = []
                films_json[film[0]]['directors'] = [{'id': film[8],'name': film[9]}]
                films_json[film[0]]['directors_names'] = [film[9]]
                films_json[film[0]]['writers'] = []
                films_json[film[0]]['writers_names'] = []

            elif film[7] == 'writer':
                films_json[film[0]]['actors'] = []
                films_json[film[0]]['actors_names'] = []
                films_json[film[0]]['directors'] = []
                films_json[film[0]]['directors_names'] = []
                films_json[film[0]]['writers'] = [{'id':film[8],'name': film[9]}]
                films_json[film[0]]['writers_names'] = [film[9]]
            elif film[7] == None:
                films_json[film[0]]['actors'] = []
                films_json[film[0]]['actors_names'] = []
                films_json[film[0]]['directors'] = []
                films_json[film[0]]['directors_names'] = []
                films_json[film[0]]['writers'] = []
                films_json[film[0]]['writers_names'] = []

            films_json[film[0]]['genre'] = [film[10]]
        else:
            if film[7] == 'actor' and {'id': film[8],'name': film[9]} not in films_json[film[0]]['actors']:
                films_json[film[0]]['actors'].append({'id': film[8],'name': film[9]})
                films_json[film[0]]['actors_names'].append(film[9])

            elif film[7] == 'director' and  {'id': film[8],'name': film[9]} not in films_json[film[0]]['directors']:
                films_json[film[0]]['directors'].append({'id': film[8],'name': film[9]})
                films_json[film[0]]['directors_names'].append(film[9])

            elif film[7] == 'writer' and {'id': film[8],'name': film[9]} not in films_json[film[0]]['writers']:
                films_json[film[0]]['writers'].append({'id':film[8],'name': film[9]})
                films_json[film[0]]['writers_names'].append(film[9])

            if film[10] not in films_json[film[0]]['genre']:
                films_json[film[0]]['genre'].append(film[10])
    return films_json
