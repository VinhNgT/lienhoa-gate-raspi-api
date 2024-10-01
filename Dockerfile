FROM python:3.11-bookworm

LABEL org.opencontainers.image.source=https://github.com/VinhNgT/lienhoa-gate-raspi-api

WORKDIR /code

COPY ./pip.conf /root/.pip/pip.conf

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
