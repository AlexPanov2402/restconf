import json
from pathlib import Path
from pyang import context, repository
from pyang import error as pyang_error
from jsonschema import validate, ValidationError


class YangManager:
    def __init__(
        self, yang_path: str = "./yang_modules", main_module: str = "jukebox.yang"
    ):
        self.yang_path = Path(yang_path).resolve()
        self.main_module = main_module
        self.repo = repository.FileRepository(str(self.yang_path))
        self.ctx = context.Context(self.repo)

        self.schema = None
        self.datastore = {}

    def load_model(self):
        module_file = str(self.yang_path / self.main_module)

        with open(module_file, "r", encoding="utf-8") as f:
            text = f.read()

        self.ctx.add_module(self.main_module, text)
        self.ctx.validate()

        self.schema = self.ctx.get_module("jukebox")
        if not self.schema:
            raise RuntimeError("Не удалось загрузить модуль jukebox")

        print("[YangManager] Модель jukebox загружена через pyang")

    def get_data(self, path: str = "") -> dict:
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
        keys = path.split("/") if path else []
        node = self.datastore

        for k in keys[:-1]:
            node = node.setdefault(k, {})

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
        try:
            validate(instance=data, schema={"type": "object"})
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации: {e.message}")
