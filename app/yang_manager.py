import json

from yangson.datamodel import DataModel
from yangson.instance import InstanceNode, InstanceRoute


class YangManager:
    def __init__(
        self, yang_path: str = "./yang_modules", lib_file: str = "library.json"
    ):
        self.yang_path = yang_path
        self.lib_file = lib_file
        self.datamodel: DataModel | None = None
        self.datastore: InstanceNode | None = None

    def load_model(self):
        with open(self.lib_file, "r", encoding="utf-8") as f:
            json.load(f)

        self.datamodel = DataModel.from_file(self.lib_file, self.yang_path)
        self.datastore = self.datamodel.get_root()

    def get_data(self, path: str = "") -> dict:
        if not self.datastore:
            raise RuntimeError("Datastore not initialized")
        if path == "":
            return self.datastore.value
        try:
            route = InstanceRoute(path.split("/"))
            node = self.datastore.goto(route)
            return node.value
        except Exception:
            raise KeyError(f"Path {path} not found in datastore")

    def patch_data(self, path: str, patch: dict) -> dict:
        if not self.datastore:
            raise RuntimeError("Datastore not initialized")

        copy = self.datastore.copy()
        try:
            route = InstanceRoute(path.split("/"))
            target = copy.goto(route)
            target.update(patch)
            self.datastore = copy
            return target.value
        except Exception as e:
            raise ValueError(f"Error in applying the PATCH: {e}")
