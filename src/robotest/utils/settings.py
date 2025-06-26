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

    def write(self):
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        with open(json_path) as file:
            json.dump(json_str, file)


settings = Settings()
