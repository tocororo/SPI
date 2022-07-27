from fastapi import APIRouter

from spi.controllers import PersonsController
from spi.models import Response, error_response_model

router = APIRouter()


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

