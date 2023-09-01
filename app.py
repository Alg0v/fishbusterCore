from json import loads
from lib import getRequestsLeft, setRequestsLeft, existsToken, createAnswer
from flask import Flask, request
from msg import MAX_REQUESTS_EXCEEDED, ERR_BAD_REQUEST, ERR_INTERNAL_DB, ERR_BAD_TOKEN, ERR_ALREADY_REPORTED, ERR_DOMAIN_WLISTED
from prediction import scanDomain
from config import api_route
from redis import Redis

app = Flask(__name__)
redisDB = Redis(host='localhost', port=6379, db=0, decode_responses=True)


@app.route(f'{api_route}domain/malicious', methods=['POST'])
def reqMalicious():
    json = loads(request.json)
    try:
        if not existsToken(json["token"]):
            return createAnswer(code=404, error=ERR_BAD_TOKEN)
        if (reqs_left := getRequestsLeft(json["token"])) <= 0:
            return createAnswer(code=403, error=MAX_REQUESTS_EXCEEDED)
        if setRequestsLeft(json["token"], reqs_left - 1):
            return createAnswer(code=500, error=ERR_INTERNAL_DB)
        return createAnswer({"level": scanDomain(json["domain"]),
                             "balance": reqs_left - 1})
    except KeyError:
        return createAnswer(code=400, error=ERR_BAD_REQUEST)


@app.route(f'{api_route}user/balance', methods=['POST'])
def reqBalance():
    json = loads(request.json)
    try:
        if not existsToken(json["token"]):
            return createAnswer(code=404, error=ERR_BAD_TOKEN)
        return createAnswer({"balance": getRequestsLeft(json["token"])})
    except KeyError:
        return createAnswer(code=400, error=ERR_BAD_REQUEST)


@app.route(f'{api_route}domain/reports', methods=['POST'])
def getDomainReports():
    json = loads(request.json)
    try:
        if not existsToken(json["token"]):
            return createAnswer(code=404, error=ERR_BAD_TOKEN)
        current_credits = int(getRequestsLeft(json["token"])) - 1
        setRequestsLeft(json["token"], current_credits)
        return createAnswer({"reports": len(redisDB.get(json["domain"]).split(";"))-1,
                             "balance": current_credits})
    except KeyError:
        return createAnswer(code=400, error=ERR_BAD_REQUEST)


@app.route(f'{api_route}domain/report', methods=['POST'])
def reportDomain():
    json = loads(request.json)
    try:
        if not existsToken(json["token"]):
            return createAnswer(code=404, error=ERR_BAD_TOKEN)
        current_credits = int(getRequestsLeft(json["token"])) - 1
        setRequestsLeft(json["token"], current_credits)
        reports = redisDB.get(json["domain"])
        if reports == "1":
            return createAnswer(code=403, error=ERR_DOMAIN_WLISTED)
        elif not json["token"] in reports.split(";"):
            redisDB.set(json["domain"], reports + json["token"] + ";")
            return createAnswer({"balance": current_credits})
        else:
            return createAnswer(code=403, error=ERR_ALREADY_REPORTED)
    except KeyError:
        return createAnswer(code=400, error=ERR_BAD_REQUEST)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
