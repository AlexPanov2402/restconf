FROM python:3.11

RUN sed -i 's|http://deb.debian.org/debian|http://mirror.yandex.ru/debian|g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|http://security.debian.org/debian-security|http://mirror.yandex.ru/debian-security|g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel \
    && pip install poetry==1.8.3

RUN poetry --version

COPY . .

RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
