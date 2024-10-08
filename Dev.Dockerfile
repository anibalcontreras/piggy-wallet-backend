FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev postgresql-dev
RUN apk add --no-cache netcat-openbsd

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --dev

COPY . /app/
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]
