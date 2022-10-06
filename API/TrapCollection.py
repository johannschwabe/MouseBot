import random
import time
from time import struct_time
from typing import Set, TYPE_CHECKING, Dict
from Trap import Trap
from os.path import exists


class TrapCollection:
    def __init__(self):
        # id -> Trap
        self.traps: Dict[str, "Trap"] = {}
        # name -> id
        self.names: Dict[str, str] = {}

    def add_trap(self, trap: "Trap"):
        self.traps[trap.id] = trap
        self.names[trap.name] = trap.id
        self.persit()

    def get_status(self):
        res = "Status:\n"
        for trap in self.traps.values():
            res += trap.get_status() + "\n"
        return res

    def get_trap(self, trap_id: str):
        if trap_id not in self.traps:
            new_name = self.next_name()
            self.add_trap(Trap(trap_id, new_name, False))
        return self.traps[trap_id]

    def next_name(self):
        count = 0
        while True:
            if f"Unknown{count}" in self.names:
                count += 1
            else:
                break
        return f"Unknown{count}"

    def remove(self, trap_name: str):
        _id = self.names[trap_name]
        del self.names[trap_name]
        del self.traps[_id]

        self.persit()

    def open(self, trap_id: str):
        trap = self.get_trap(trap_id)
        trap.change(_open=True)
        self.persit()

    def close(self, trap_id: str):
        trap = self.get_trap(trap_id)
        trap.change(_open=False)
        self.persit()
        return trap

    def healthcheck(self, trap_id: str, _open: bool):
        self.get_trap(trap_id).healthcheck_success(_open)
        self.persit()

    def rename(self, trap_name: str, new_name: str):
        _id = self.names[trap_name]
        trap = self.get_trap(_id)
        trap.name = new_name
        del self.names[trap_name]
        self.names[new_name] = _id

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
                        new_trap_collection.traps[recovered_trap.id] = recovered_trap
                        new_trap_collection.names[recovered_trap.name] = recovered_trap.id

                break
            else:
                current_timestamp -= 24 * 60 * 60
        return new_trap_collection


def filename_for_date(time_struct: "struct_time"):
    return f"persistence/Trapy-{time_struct.tm_year}{time_struct.tm_mon}{time_struct.tm_mday}"
