from fastapi import APIRouter

from Controllers.collectPersons import CollectPersonsController
from Controllers.personController import PersonsController

from database import (Response, error_response_model)

router = APIRouter()


@router.get("/persons")
async def get_all():
    persons = await PersonsController.retrieve()
    return Response(code=200, status="Ok", message="Success retrieve all data", result=persons).dict(exclude_none=True)


@router.post("/persons/collect")
async def create():
    person = await CollectPersonsController.get_assets_list_persons()
    return Response(code=200, status="Ok", message="Success save data", result=person).dict(exclude_none=True)


@router.get("/persons/{id}")
async def get_one(id: str):
    person = await PersonsController.retrieve_person(id)
    return Response(code=200, status="Ok", message="Success retrieve data", result=person).dict(exclude_none=True)
