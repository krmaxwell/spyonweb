import os

import requests


class spyonweb(object):

    def __init__(self, token, url=None):
        self.token = token
        if url:
            self.url = url
        else:
            self.url = "https://api.spyonweb.com/v1/"

    def summary(self, domain_name):
        data = requests.get(self.url + "summary/" + domain_name + "?access_token=" + self.token)
        return data.json()

    def domain(self, domain_name):
        data = requests.get(self.url + "domain/" + domain_name + "?access_token=" + self.token)
        return data.json()

    def analytics(self, code, limit=None):
        data = requests.get(self.url + "analytics/" + code + "?access_token=" + self.token + "&limit=" + limit)
        # TODO: implement paging
        return data.json()


def main():
    token = os.getenv("SPYONWEB_API")
    s = spyonweb(token=token)
    a = "UA-34505845"
    print s.analytics(a)


if __name__ == "__main__":
    main()
