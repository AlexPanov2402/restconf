# RESTCONF Server on FastAPI

Тестовый проект: учебная реализация **RESTCONF-сервера** на базе [FastAPI](https://fastapi.tiangolo.com/) с поддержкой YANG-моделей.  
В качестве примера используется модель [`jukebox.yang`](yang_modules/jukebox.yang) из [RFC 8040](https://datatracker.ietf.org/doc/html/rfc8040).

## 🚀 Возможности
- Работа по RESTCONF API с использованием YANG-моделей.
- Поддержка операций:
  - `GET`: получение данных.
  - `PATCH`: обновление данных.
  - `POST`: выполнение операций RPC.
- Swagger UI для тестирования: `/docs`.

---

## 🔧 Установка и запуск

### Локально (через Poetry)

1. Установите Poetry, если ещё не установлен:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
Установите зависимости проекта:

bash
Копировать код
poetry install
Запустите сервер:

bash
Копировать код
poetry run uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
Откройте в браузере:

Swagger UI: http://127.0.0.1:8000/docs

OpenAPI: http://127.0.0.1:8000/openapi.json

В Docker
Соберите и запустите контейнер:

bash
Копировать код
docker compose build
docker compose up -d
После запуска сервер доступен:

Локально: http://127.0.0.1:8000/docs

По сети (например, на внешнем IP): http://<SERVER_IP>:8000/docs

⚠️ Убедитесь, что порт открыт в firewall:

bash
Копировать код
sudo ufw allow 8000/tcp
📡 Примеры HTTP-запросов
1. GET: Получить все данные из datastore
bash
Копировать код
curl http://127.0.0.1:8000/restconf/data
2. GET: Получить конкретный узел по пути /restconf/data/<path>
bash
Копировать код
curl http://127.0.0.1:8000/restconf/data/jukebox/library/album
3. PATCH: Изменить данные (например, добавить альбом)
bash
Копировать код
curl -X PATCH http://127.0.0.1:8000/restconf/data/jukebox/library \
  -H "Content-Type: application/json" \
  -d '{"album":[{"name":"BestOf","artist":"Queen"}]}'
4. POST: Вызвать RPC-метод (например, воспроизвести песню)
bash
Копировать код
curl -X POST http://127.0.0.1:8000/restconf/operations/play-song \
  -H "Content-Type: application/json" \
  -d '{"song": "Bohemian Rhapsody"}'
✅ Проверка работы основных методов
GET на корень datastore: /restconf/data возвращает всё хранилище или конкретный узел по пути /restconf/data/<path>.

Пример: GET /restconf/data/jukebox/library вернёт данные о коллекции альбомов.

PATCH: Изменяет данные, и изменения видны при последующем GET.

Пример: добавление нового альбома через PATCH должно отобразиться в GET.

POST на RPC-эндпоинт: Вызывает соответствующий метод-обработчик и возвращает результат.

Пример: POST /restconf/operations/play-song вернёт статус исполнения команды.

🛠️ Технологии
Python 3.11

FastAPI + Uvicorn

Poetry (управление зависимостями)

Docker + docker-compose

pyang, yangson (работа с YANG)

🔮 Перспективы развития
Хранение данных в PostgreSQL.

Кэширование в Redis.

Авторизация (OAuth2/JWT).

Дополнительные YANG-модели.

Тестирование (pytest) и CI.