import json
from pathlib import Path
from pyang import context, repository
from pyang import error as pyang_error
from jsonschema import validate, ValidationError


class YangManager:
    """
    Класс для работы с YANG-моделями и in-memory datastore.

    - Загружает YANG-модуль через pyang.
    - Хранит данные в памяти (dict).
    - Позволяет читать и изменять данные по пути.
    - Выполняет базовую валидацию json-данных.
    """

    def __init__(
        self, yang_path: str = "./yang_modules", main_module: str = "jukebox.yang"
    ):
        """
        :param yang_path: Путь к директории с YANG-модулями.
        :param main_module: Имя основного YANG-модуля.
        """
        self.yang_path = Path(yang_path).resolve()
        self.main_module = main_module

        # Репозиторий и контескт для работы с YANG через pyang
        self.repo = repository.FileRepository(str(self.yang_path))
        self.ctx = context.Context(self.repo)

        # Хранилище схемы и данных (in-memory)
        self.schema = None
        self.datastore = {}

    def load_model(self):
        """
        Загружает основной YANG-модуль и валидирует его.

        :raises RuntimeError: если модуль не удалось загрузить.
        """
        module_file = str(self.yang_path / self.main_module)

        # Читаем текст YANG-модуля
        with open(module_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Добавляем модуль в pyang-контекст
        self.ctx.add_module(self.main_module, text)
        self.ctx.validate()

        # Сохраняем схему
        self.schema = self.ctx.get_module("jukebox")
        if not self.schema:
            raise RuntimeError("Не удалось загрузить модуль jukebox")

        print("[YangManager] Модель jukebox загружена через pyang")

    def get_data(self, path: str = "") -> dict:
        """
        Получает данные из in-memory datastore по указанному пути.

        :param path: путь вида 'jukebox/library/album'
        :return: данные (dict или подузел)
        :raises KeyError: если путь не найден.
        """
        if path == "":
            return self.datastore

        keys = path.split("/")
        node = self.datastore

        for k in keys:
            if not k:
                continue
            if k not in node:
                raise KeyError(f"Path {path} not found in datastore")
            node = node[k]

        return node

    def patch_data(self, path: str, patch: dict) -> dict:
        """
        Применяет PATCH-обновления данных.

        :param path: путь в виде строки ('jukebox/library')
        :param patch: словарь с изменениями
        :return: обновлённый фрагмент datastore
        """
        keys = path.split("/") if path else []
        node = self.datastore

        # Проходим по иерархии, создаём узлы при необходимости
        for k in keys[:-1]:
            node = node.setdefault(k, {})

        # Вставляем или обновляем данные
        if keys:
            target_key = keys[-1]
            if target_key not in node:
                node[target_key] = {}
            if isinstance(node[target_key], dict):
                node[target_key].update(patch)
            else:
                node[target_key] = patch
            result = node[target_key]
        else:
            self.datastore.update(patch)
            result = self.datastore

        return result

    def validate_data(self, data: dict):
        """
        Валидирует json-данные.

        :param data: словарь с данными
        :raises ValueError: если данные не проходят валидацию
        """
        try:
            validate(instance=data, schema={"type": "object"})
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации: {e.message}")
