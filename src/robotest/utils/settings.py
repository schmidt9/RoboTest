import json
import os.path
from pathlib import Path
from dataclasses import dataclass, asdict

json_path = os.path.join(Path(__file__).parent, "settings.json")


@dataclass
class Settings:
    speed_left: int
    speed_right: int
    speed_turn: int

    @staticmethod
    def read():
        with open(json_path) as file:
            dict = json.load(file)
            settings = Settings(**dict)
            return settings

    def toJSON(self):
        dict = asdict(self)
        return json.dumps(
            dict,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        )

    def write(self):
        dict = asdict(self)

        with open(json_path, "w") as file:
            json.dump(dict, file, sort_keys=True, ensure_ascii=False, indent=4)


settings = Settings.read()
