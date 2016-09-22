import os
from argparse import ArgumentParser

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
    parser = ArgumentParser()
    parser.add_argument('-s', '--summary', type=str, help="Specify a domain for the Request Summary API")
    parser.add_argument('-d', '--domain', type=str, help="Specify a domain for the Domain API")
    parser.add_argument('-a', '--analytics', type=str, help="Specify a code for the Analytics API")
    args, _ = parser.parse_known_args()

    token = os.getenv("SPYONWEB_API")
    s = spyonweb(token=token)

    if args.summary:
        print s.summary(args.summary)
    if args.domain:
        print s.domain(args.domain)
    if args.analytics:
        print s.analytics(args.analytics)


if __name__ == "__main__":
    main()
