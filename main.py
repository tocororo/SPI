#!/usr/bin/env python
import uvicorn
from fastapi import FastAPI

from Routes.persons import router as PersonRouter

app = FastAPI()

app.include_router(PersonRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
