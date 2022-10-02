from fastapi import HTTPException, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import telegram

from APIObjects import APITrap, APIName, APINameChange, APIId
from Trap import Trap
from TrapCollection import TrapCollection

f = open("../.secrets", "r")
token = f.readlines()[0]
bot = telegram.Bot(token)

t = open("../chat_ids.txt", "r")
chat_ids = [int(_id) for _id in t.readlines()]

trap_collection = TrapCollection.recover()

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5050",
    "*",  # REMOVE for production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/catch")
def catch(_catch: "APIId"):
    trap = trap_collection.close(_catch.trap_id)
    for chat_id in chat_ids:
        bot.send_message(text=f"🐭 in {trap.name}", chat_id=chat_id)


@app.post("/open")
def reopen(_catch: "APIId"):
    trap_collection.open(_catch.trap_id)


@app.post("/register")
def register(trap: "APITrap"):
    new_trap = Trap(trap.trap_id, trap_collection.next_name(), trap.open)
    trap_collection.add_trap(new_trap)


@app.post("/healthcheck")
def healthcheck(trap: "APITrap", ):
    trap_collection.healthcheck(trap.trap_id, trap.open)

@app.post("/remove")
def remove(trap: "APIName"):
    trap_collection.remove(trap.trap_name)

@app.post("/clear")
def clear():
    trap_collection.clear()

@app.post("/rename")
def rename(change: "APINameChange"):
    trap_collection.rename(change.old, change.new)


@app.get("/status")
def status():
    return {"status": trap_collection.get_status()}
