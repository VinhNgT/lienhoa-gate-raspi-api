from fastapi import FastAPI, HTTPException, status
from modules import status_lights, gate, screen, buzzer, distance_sensor
from modules.exceptions import app_exceptions

app = FastAPI(
    title="LienHoa auto parking gate",
    version="1.0.0",
    summary="API điều khiển module Raspberry Pi Zero 2 cho dự án cổng tự động.",
    contact={
        "name": "Nguyễn Thế Vinh",
        "url": "https://github.com/VinhNgT",
        "email": "victorpublic0000@gmail.com",
    },
)

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
