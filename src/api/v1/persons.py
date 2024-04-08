from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query, Depends, Response, HTTPException

from src.services.person import PersonService, get_person_service
from src.models.models import Person
from src.api.v1.films import get_pagination_params


router = APIRouter()


@router.get(
    '/search',
    response_model=Optional[list[Person]],
    summary='Get persons by searching using keyword in the name of the person'
)
async def search_persons(
    pagination: Annotated[dict, Depends(get_pagination_params)],
    query: Annotated[str, Query(description='Person')] = None,
    person_service: PersonService = Depends(get_person_service),
):
    """
        Get person list:

        Parameters:
            **query** (str): keyword to search a person
            **page_number** (int): page number
            **page_size** (int): number of films per page
            **pagination**: a dependency that returns the pagination parameters -
            page_number (int, default=0), page_size (int, default=10)
        Return value:
            **persons** (Optional[list[Person]]): list of persons
    """

    page_number = pagination['page_number']
    page_size = pagination['page_size']

    persons = await person_service.search_persons(
        page_number,
        page_size,
        query,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Persons not found'
        )
    return persons


@router.get(
    '/{person_id}',
    response_model=Optional[Person],
    summary='Get person details by person id'
)
async def person_details(
    response: Response,
    person_id: Annotated[str, Path(default=...)],
    person_service: PersonService = Depends(get_person_service)
):
    """
        Get person details by person id:

        Parameters:
            **person_id** (str): person id

        Return value:
            **person** (Optional[Person]): person with the following fields:
            id, full_name, films
    """

    person = await person_service.get_person_by_id(person_id, response)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Person not found'
        )
    return person
