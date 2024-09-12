from fastapi import FastAPI, HTTPException, status
from modules import status_lights, gate

app = FastAPI()

app.include_router(status_lights.router)
app.include_router(gate.router)


@app.exception_handler(ValueError)
async def value_exception_handler(request, exc):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))
