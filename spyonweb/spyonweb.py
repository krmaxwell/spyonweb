import requests


class spyonweb(object):

    def __init__(self, token, url=None):
        self.token = token
        if url:
            self.url = url
        else:
            self.url = "https://api.spyonweb.com/v1/"

    def summary(self, domain):
        data = requests.get(self.url + "summary/" + domain + "?access_token=" + self.token)
        return data
