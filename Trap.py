import math
import time


class Trap:
    def __init__(self, name: str, _open: bool):
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

    def healthcheck_success(self, _open: bool):
        self.health_check = time.time()
        self.open = _open

    def change(self, _open: bool):
        self.open = _open
        self.latest_change = time.time()
        self.health_check = time.time()

    def __eq__(self, other):
        assert isinstance(other, Trap)
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.name}|{self.open}|{self.latest_change}|{self.health_check}"

    @staticmethod
    def recover(stringified: str):
        split = stringified.split("|")
        assert len(split) == 4
        new_trap = Trap(split[0], split[1] == "True")
        new_trap.latest_change = float(split[2])
        new_trap.health_check = float(split[3])
        return new_trap

