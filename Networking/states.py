from enum import Enum


class ClientState(Enum):
    READY = 1
    CONNECTED = 2
    SOLVING = 3
    SOLVED = 4
    WAITING = 5
    APPROVED = 6
    REJECTED = 7


class ServerState(Enum):
    READY = 1
    CONNECTED = 2
    WAITING = 3
    CHECKING = 4
    CHECKED = 5
