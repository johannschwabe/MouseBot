import math
import time


class Trap:
    def __init__(self, _id: str, name: str, _open: bool, voltage: float):
        self.id = _id
        self.name = name
        self.open = _open
        self.voltage = voltage
        self.latest_change = time.time()
        self.health_check = time.time()

    def is_alive(self):
        return (time.time() - self.health_check) / (60*60) < 1

    def get_status(self):
        catch = '❌' if self.open else ('🐭' + "!" * math.floor((self.latest_change - time.time()) / (60*60)))
        healthcheck = '🟢' if self.is_alive() else '🔴'
        return f"{self.name}: Catch: {catch}, responding: {healthcheck}, {self.voltage:.2f}V"

    def healthcheck_success(self, _open: bool):
        self.health_check = time.time()
        self.open = _open
        print(f"Health checked: {self.name}, {'open' if self.open else 'closed'}")

    def change(self, _open: bool):
        self.open = _open
        self.latest_change = time.time()
        self.health_check = time.time()

    def __eq__(self, other):
        assert isinstance(other, Trap)
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id}|{self.name}|{self.open}|{self.latest_change}|{self.health_check}|{self.voltage:.2f}"

    @staticmethod
    def recover(stringified: str):
        split = stringified.split("|")
        assert len(split) == 6
        new_trap = Trap(split[0],split[1], split[2] == "True", float(split[5]))
        new_trap.latest_change = float(split[3])
        new_trap.health_check = float(split[4])
        return new_trap

