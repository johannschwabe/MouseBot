import time
from time import struct_time
from typing import Set, TYPE_CHECKING, Dict
from Trap import Trap
from os.path import exists


class TrapCollection:
    def __init__(self):
        self.traps: Dict[str, "Trap"] = {}

    def add_trap(self, trap: "Trap"):
        self.traps[trap.id] = trap
        self.persit()

    def get_status(self):
        res = ""
        for trap in self.traps.values():
            res += trap.get_status() + "\n"
        return res

    def get_trap(self, trap_id: str):
        if trap_id not in self.traps:
            self.add_trap(Trap(trap_id, "Unknown", False))
        return self.traps[trap_id]

    def remove(self, trap_id: str):
        del self.traps[trap_id]
        self.persit()

    def open(self, trap_id: str):
        trap = self.get_trap(trap_id)
        trap.change(_open=True)
        self.persit()

    def healthcheck(self, trap_id: str, _open: bool):
        self.get_trap(trap_id).healthcheck_success(_open)
        self.persit()

    def rename(self, trap_id: str, trap_name: str):
        self.get_trap(trap_id).name = trap_name
        self.persit()

    def persit(self):
        filename = filename_for_date(time.localtime())
        with open(filename, "w") as file:
            for trap in self.traps.values():
                print(str(trap))
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
                break
            else:
                current_timestamp -= 24 * 60 * 60
        return new_trap_collection


def filename_for_date(time_struct: "struct_time"):
    return f"persistence/Trapy-{time_struct.tm_year}{time_struct.tm_mon}{time_struct.tm_mday}"
