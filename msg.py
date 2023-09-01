from json import dumps
from config import url, docsurl

MAX_REQUESTS_EXCEEDED = "You exceeded your maximum number of requests. You'll be given new requests tomorrow."

ERR_BAD_REQUEST       = f'Bad request, information is missing. You can read the docs for the api at {docsurl}'

ERR_INTERNAL_DB       = "There was an internal error regarding our database. Please consider retrying in a few moments."

ERR_BAD_TOKEN         = f'The token you provided doesn\'t exist on our database at {url}. Make sure you didn\'t make ' +\
                         'a typo while setting up your extension.'

ERR_ALREADY_REPORTED  = f'You already reported that domain.'

ERR_DOMAIN_WLISTED    = f'This domain has been whitelisted by the administrator of your fishbuster instance ({url}).'

SPECIAL_MSG           = ""
