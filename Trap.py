import math
import time


class Trap:
    def __init__(self, _id: "str", name: str, _open: bool):
        self.id = _id
        self.name = name
        self.open = _open
        self.latest_change = time.time()
        self.health_check = time.time()

    def is_alive(self):
        return (time.time() - self.health_check) / (60*60) < 1

    def get_status(self):
        catch = '❌' if self.open else ('🐭' + "!" * math.floor((self.latest_change - time.time()) / (60*60)))
        healthcheck = '🟢' if self.is_alive() else '🔴'
        return f"{self.name}: Catch: {catch}, responding: {healthcheck}"

    def healthcheck_success(self):
        self.health_check = time.time()

    def change(self, _open: bool):
        self.open = _open
        self.latest_change = time.time()
        self.health_check = time.time()

    def __eq__(self, other):
        assert isinstance(other, Trap)
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)