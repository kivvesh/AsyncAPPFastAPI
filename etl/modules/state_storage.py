import json
from typing import Any, Dict


class JsonFileStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        with open(self.file_path, 'r') as file:
            try:
                json_file = json.load(file)
            except:
                json_file = None
        return json_file

class State:
    def __init__(self, storage: JsonFileStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        storage = self.storage.retrieve_state()
        storage[key] = value
        self.storage.save_state(storage)


    def get_state(self, key: str) -> Any:
        try:
            state_dict = self.storage.retrieve_state()
            return state_dict[key]
        except:
            return None