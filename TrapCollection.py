import random
import time
from time import struct_time
from typing import Set, TYPE_CHECKING, Dict
from Trap import Trap
from os.path import exists


class TrapCollection:
    def __init__(self):
        self.traps: Dict[str, "Trap"] = {}

    def add_trap(self, trap: "Trap"):
        self.traps[trap.name] = trap
        self.persit()

    def get_status(self):
        res = ""
        for trap in self.traps.values():
            res += trap.get_status() + "\n"
        return res

    def get_trap(self, trap_name: str):
        if trap_name not in self.traps:
            count = 0
            while True:
                if f"Unknown{count}" in self.traps:
                    count += 1
                else:
                    break
            self.add_trap(Trap(f"Unknown{count}", False))
        return self.traps[trap_name]

    def remove(self, trap_name: str):
        del self.traps[trap_name]
        self.persit()

    def open(self, trap_name: str, _open: bool):
        trap = self.get_trap(trap_name)
        trap.change(_open)
        self.persit()

    def healthcheck(self, trap_name: str, _open: bool):
        self.get_trap(trap_name).healthcheck_success(_open)
        self.persit()

    def rename(self, trap_name: str, new_name: str):
        trap = self.traps.pop(trap_name)
        trap.name = new_name
        self.add_trap(trap)

    def persit(self):
        filename = filename_for_date(time.localtime())
        with open(filename, "w") as file:
            for trap in self.traps.values():
                file.write(str(trap) + "\n")

    @staticmethod
    def recover():
        new_trap_collection = TrapCollection()
        current_timestamp = time.time()
        max_attempts = 400
        _iter = 0
        while _iter < max_attempts:
            _iter += 1
            time_struct = time.localtime(current_timestamp)
            potential_filename = filename_for_date(time_struct)
            if exists(potential_filename):
                with open(potential_filename) as file:
                    for line in file.readlines():
                        recovered_trap = Trap.recover(line)
                        new_trap_collection.traps[recovered_trap.name] = recovered_trap
                break
            else:
                current_timestamp -= 24 * 60 * 60
        return new_trap_collection


def filename_for_date(time_struct: "struct_time"):
    return f"persistence/Trapy-{time_struct.tm_year}{time_struct.tm_mon}{time_struct.tm_mday}"
