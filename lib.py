from redis import Redis
from msg import SPECIAL_MSG
from json import dumps

usersDB = Redis(host='localhost', port=6379, db=1)


def getRequestsLeft(token):
    return int(usersDB.get(token) or -1)


def setRequestsLeft(token, rleft):
    return not usersDB.set(token, rleft)  # False if no errors, True if errors


def existsToken(token):
    return bool(int(usersDB.get(token) or -1) + 1)


def createAnswer(additional_json: dict = None, code: int = 200, msg: str = SPECIAL_MSG, error: str = ""):
    json = {
        "code": code,
        "msg": msg,
        "error": error
    }
    for key in list(additional_json or {}):
        json[key] = additional_json[key]
    return dumps(json)
