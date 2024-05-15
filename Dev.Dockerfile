FROM python:3.11-alpine

WORKDIR /app

# Instalar paquetes necesarios para construir psycopg2 y otras dependencias, y netcat para comprobar la conexión de la base de datos
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev postgresql-dev
RUN apk add --no-cache netcat-openbsd

# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Install application dependencies
COPY Pipfile Pipfile.lock /app/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments.
RUN pipenv install --system --dev

COPY . /app/
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]
