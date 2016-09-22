import os
import pprint
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
        full_url = self.url + "analytics/" + code + "?access_token=" + self.token
        if limit:
            full_url = full_url + "&limit=" + str(limit)
        data = requests.get(full_url)
        # TODO: implement paging
        return data.json()

    def ipaddress(self, ipaddr, limit=None):
        full_url = self.url + "ip/" + ipaddr + "?access_token=" + self.token
        if limit:
            full_url = full_url + "&limit=" + str(limit)
        data = requests.get(full_url)
        # TODO: implement paging
        return data.json()

    def dns_domain(self, name, limit=None):
        full_url = self.url + "dns_domain/" + name + "?access_token=" + self.token
        if limit:
            full_url = full_url + "&limit=" + str(limit)
        data = requests.get(full_url)
        # TODO: implement paging
        return data.json()

    def ip_dns(self, ipaddr, limit=None):
        full_url = self.url + "ip_dns/" + ipaddr + "?access_token=" + self.token
        if limit:
            full_url = full_url + "&limit=" + str(limit)
        data = requests.get(full_url)
        # TODO: implement paging
        return data.json()


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--summary', type=str, help="Specify a domain for the Request Summary API")
    parser.add_argument('-d', '--domain', type=str, help="Specify a domain for the Domain API")
    parser.add_argument('-a', '--analytics', type=str, help="Specify a code for the Analytics API")
    parser.add_argument('-i', '--ipaddress', type=str, help="Specify an address for the IP Address API")
    parser.add_argument('-n', '--dns_domain', type=str, help="Specify a name for the Domains on Nameserver API")
    parser.add_argument('-p', '--ip_dns', type=str, help="Specify an address for the Nameservers on IP Address API")
    args, _ = parser.parse_known_args()

    pp = pprint.PrettyPrinter(indent=2)

    token = os.getenv("SPYONWEB_API")
    s = spyonweb(token=token)

    if args.summary:
        pp.pprint(s.summary(args.summary))
    if args.domain:
        pp.pprint(s.domain(args.domain))
    if args.analytics:
        pp.pprint(s.analytics(args.analytics))
    if args.ipaddress:
        pp.pprint(s.ipaddress(args.ipaddress))
    if args.dns_domain:
        pp.pprint(s.dns_domain(args.dns_domain))
    if args.ip_dns:
        pp.pprint(s.ip_dns(args.ip_dns))


if __name__ == "__main__":
    main()
