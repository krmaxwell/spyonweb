import os

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
        return data.json()


def main():
    token = os.getenv("SPYONWEB_API")
    s = spyonweb(token=token)
    d = "fullmooncalendar.net"
    print s.summary(d)


if __name__ == "__main__":
    main()
