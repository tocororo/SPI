#!/usr/bin/env python
import uvicorn

from spi import create_app
from spi.database import close, connect

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
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
