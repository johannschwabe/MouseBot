from typing import Set, TYPE_CHECKING, Dict
from Trap import Trap


class TrapCollection:
    def __init__(self):
        self.traps: Dict[str,"Trap"] = {}

    def add_trap(self, trap: "Trap"):
        self.traps[trap.id] = trap

    def get_status(self):
        res = ""
        for trap in self.traps.values():
            res += trap.get_status() + "\n"
        return res

    def get_trap(self, trap_id: str):
        if trap_id not in self.traps:
            self.traps[trap_id] = Trap(trap_id, "Unknown", False)
        return self.traps[trap_id]

    def remove(self, trap_id: str):
        del self.traps[trap_id]