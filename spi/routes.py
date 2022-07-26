from fastapi import APIRouter

from spi.controllers import PersonsController
from spi.models import Response

router = APIRouter()


@router.get("/persons")
async def get_all():
    persons = await PersonsController.retrieve()
    return Response(
        code=200, status="Ok", message="Success retrieve all data", result=persons
        ).dict(exclude_none=True)


@router.get("/persons/{id}")
async def get_one(id: str):
    person = await PersonsController.retrieve_person(id)
    return Response(code=200, status="Ok", message="Success retrieve data", result=person).dict(
        exclude_none=True
        )
