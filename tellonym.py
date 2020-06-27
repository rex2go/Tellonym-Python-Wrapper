import requests
import json
import random 
from collections import namedtuple

class Tellonym:
    authorizationKey = None

    def __init__(self, authorizationKey):
        self.authorizationKey = authorizationKey

    def tell(self, userId, tell):
        return self.apiRequest("tells/create", '{"userId": ' + str(userId) + ', "tell": "' + tell + '", "limit": 25}')

    def answerTell(self, tellId, answer):
        return self.apiRequest("answers/create", '{"answer": "' + answer + '", "limit": 25, "tellId": ' + str(tellId) + '}')

    def getUser(self, name, limit = 25):
        data = self.apiRequest("profiles/name/" + name + "?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))

    def getTells(self, limit = 25):
        data = self.apiRequest("tells?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())).tells
    
    def getAnswers(self, limit = 25):
        return self.getSelf().answers

    def getSuggestions(self, limit = 25):
        data = self.apiRequest("suggestions/people?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())).peopleSuggestions

    def getSelf(self):
        data = self.apiRequest("accounts/myself", None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))

    def getFeed(self, limit = 25):
        data = self.apiRequest("feed/list?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))

    def getFriends(self, limit = 25):
        data = self.apiRequest("suggestions/friends?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())).friends

    def getNotifications(self, limit = 25):
        data = self.apiRequest("notifications?limit=" + str(limit), None, [], "get")
        return json.loads(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())).notifications

    def apiRequest(self, param, data = None, headers = [], method = "post"):
        header = {"content-type": "application/json;charset=utf-8", "Authorization": "Bearer " + self.authorizationKey}

        for head in headers:
            header.update({head[0]: head[1]})

        if method == "post":
            r = requests.post("https://api.tellonym.me/" + param, data = data.encode('utf-8'), headers = header)
        elif method == "get":
            r = requests.get("https://api.tellonym.me/" + param, data = data, headers = header)

        if r.status_code != 200:
            return str(r.status_code) + " " + r.reason
        return r.text

