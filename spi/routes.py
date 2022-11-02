from fastapi import APIRouter
import requests
from requests.adapters import HTTPAdapter, Retry

from spi.controllers import PersonsController
from spi.models import Response, error_response_model

router = APIRouter()

def make_request(url: str = '', headers: dict = {}, params: dict = {}):
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url, headers=headers, params=params)
    return response

@router.get("/persons")
async def get_all():
    persons = await PersonsController.retrieve()
    return Response(
        code=200, status="Ok", message="Success retrieve all data", result=persons
        ).dict(exclude_none=True)


@router.get("/person")
async def get_one(idExpediente: str):
    person = await PersonsController.retrieve_person(idExpediente)
    if person:
        return Response(code=200, status="Ok", message="Success retrieve data", result=person).dict(
            exclude_none=True
            )
    else:
        return error_response_model('not Found', 404, "Pids not found")

