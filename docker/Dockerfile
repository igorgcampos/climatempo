FROM python:3.10.13-alpine

WORKDIR ./src
COPY ../assets ./assets
COPY ../climatempo ./climatempo
COPY ../pyproject.toml ./
COPY ../poetry.lock ./
COPY ../README.md ./
COPY ../.env ./

RUN pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction

CMD ["poetry", "run", "python", "./climatempo/main.py"]