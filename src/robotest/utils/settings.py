import json


class Settings:

    def __init__(self) -> None:
        json_obj = self.read()
        self.speed_left: str = json_obj.speed.left
        self.speed_right: str = json_obj.speed.left
        self.speed_turn: str = json_obj.speed.turn

    def read(self):
        with open("settings.json") as file:
            return json.load(file)

    def write(self):
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        with open("settings.json") as file:
            json.dump(json_str, file)


settings = Settings()
