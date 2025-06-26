import json
import os.path
from pathlib import Path

json_path = os.path.join(Path(__file__).parent, "settings.json")


class Settings:

    def __init__(self) -> None:
        json_dict = self.read()
        self.speed_left: str = json_dict["speed"]["left"]
        self.speed_right: str = json_dict["speed"]["right"]
        self.speed_turn: str = json_dict["speed"]["turn"]

    def read(self):
        with open(json_path) as file:
            return json.load(file)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def write(self):
        with open(json_path) as file:
            json.dump(self.toJSON(), file)


settings = Settings()
