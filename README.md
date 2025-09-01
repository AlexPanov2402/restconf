# RESTCONF Server on FastAPI

Тестовый проект: реализация **RESTCONF-сервера** на базе [FastAPI](https://fastapi.tiangolo.com/) с поддержкой YANG-моделей.  

В качестве примера используется модель [`jukebox.yang`](yang_modules/jukebox.yang) из [RFC 8040](https://datatracker.ietf.org/doc/html/rfc8040).

Для создания виртуального окружения и работы с зависимостями используем poetry.

Рабочий вариант проекта запущен на удалённом сервере (ubuntu 24.02) с помощью контейнеризации docker.

Запросы на сервер временно доступны по адресу http://92.242.60.28:8000/docs. 

## Используемый стек:
Python 3.11
FastAPI (swager api) + Uvicorn
Poetry (управление зависимостями)
Docker + docker-compose
pyang, yangson (работа с YANG)

## Возможности
- Работа по RESTCONF API с использованием YANG-моделей.
- Поддержка операций:
  - `GET`: получение данных.
  - `PATCH`: обновление данных.
  - `POST`: выполнение операций RPC.
- Используем open api (Swagger UI) для тестирования: `/docs`.
---
## Установка и запуск
Возможно через poetry (рекомендую), pip, docker.  

Создаём/выбираем рабочую директорию.
Инициализируем git:
```
git init
```
Клонируем репозиторий:
```
git clone https://github.com/AlexPanov2402/restconf.git
```
Зайдите в корневую директорию проекта.
Создайте .env вручную или используйте команду (для ubuntu):
```
cat > .env <<EOF
HOST=0.0.0.0
PORT=8000
EOF
```
---
## Через poetry

Инициализируем poetry:
```
install poetry
``` 
Запускаем сервер:
```
poetry run uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
```

Откройте в браузере:

Swagger UI: http://127.0.0.1:8000/docs

OpenAPI: http://127.0.0.1:8000/openapi.json

---

## Через pip
Устанавливаем виртуалку:
```
python3 -m venv .venv
```
Заходим в виртуалку:
```
source .venv/bin/activate
```
Устанавливаем зависимости:
```
pip install -r requirements.txt
```
Запускаем сервер:
```
python -m uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
```

---

## С помощью Docker
Собераем и запускаем контейнер:
```
docker compose build
docker compose up -d
```
После запуска сервер доступен:

Локально: http://127.0.0.1:8000/docs

---

## Примеры HTTP-запросов
1. GET: Получить все данные из datastore
```
curl http://127.0.0.1:8000/restconf/data
```
2. GET: Получить конкретный узел по пути /restconf/data/<path>
```
curl http://127.0.0.1:8000/restconf/data/jukebox/library/album
```
3. PATCH: Изменить данные
```
curl -X PATCH http://127.0.0.1:8000/restconf/data/jukebox/library \
  -H "Content-Type: application/json" \
  -d '{"album":[{"name":"BestOf","artist":"Queen"}]}'
```
4. POST: Вызвать RPC-метод
```
curl -X POST http://127.0.0.1:8000/restconf/operations/play-song \
  -H "Content-Type: application/json" \
  -d '{"song": "Bohemian 
```

##### PATCH: Изменяет данные, изменения видны при последующем GET.

##### POST: на RPC-эндпоинт вызывает соответствующий метод-обработчик.