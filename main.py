#!/usr/bin/env python
import uvicorn, os

from spi import create_app
from spi.database import close, connect

API_HOST = os.getenv('API_HOST')
API_PORT = int(os.getenv('API_PORT'))

app = create_app()

@app.on_event("startup")
async def on_app_start():
    """Anything that needs to be done while app starts
    """
    await connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    """Anything that needs to be done while app shutdown
    """
    await close()

if __name__ == '__main__':
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
