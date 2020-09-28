FROM python:3.8-alpine

RUN apk add gcc linux-headers musl-dev make postgresql-dev python3-dev libffi-dev

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt
COPY . /code

CMD ["sh", "runner.sh"]
