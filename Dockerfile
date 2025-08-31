FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "python", "app/server.py"]