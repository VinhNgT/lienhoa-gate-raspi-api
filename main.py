from fastapi import FastAPI, HTTPException, status
from modules import status_lights, gate, screen, buzzer, distance_sensor
from modules.exceptions import app_exceptions

app = FastAPI()

app.include_router(status_lights.router)
app.include_router(gate.router)
app.include_router(screen.router)
app.include_router(buzzer.router)
app.include_router(distance_sensor.router)


@app.exception_handler(ValueError)
async def value_exception_handler(request, exc):
    raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))


@app.exception_handler(app_exceptions.TooManyRequestsException)
async def buzzer_too_many_requests_exception_handler(request, exc):
    raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc))
