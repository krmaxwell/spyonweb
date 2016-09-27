import json
import os
import pprint
import sys
from argparse import ArgumentParser
from collections import OrderedDict

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
        return json.dumps(self._fetch(endpoint='analytics', query=code, limit=limit))

    def adsense(self, code, limit=None):
        return json.dumps(self._fetch(endpoint='adsense', query=code, limit=limit))

    def ipaddress(self, ipaddr, limit=None):
        return json.dumps(self._fetch(endpoint='ip', query=ipaddr, limit=limit))

    def dns_domain(self, name, limit=None):
        return json.dumps(self._fetch(endpoint='dns_domain', query=name, limit=limit))

    def ip_dns(self, ipaddr, limit=None):
        return json.dumps(self._fetch(endpoint='ip_dns', query=ipaddr, limit=limit))

    def _fetch(self, endpoint, query, limit):
        full_url = self.url + endpoint + "/" + query + "?access_token=" + self.token
        fetched = 0              # records retrieved in last batch
        found = 0                # records available in total
        results = OrderedDict()  # dict of domain and dates

        if limit:
            full_url = full_url + "&limit=" + str(limit)
        else:
            limit = sys.maxint

        new_url = full_url
        while fetched <= min(limit, found):
            data = requests.get(new_url).json(object_pairs_hook=OrderedDict)
            if data['status'] != 'found':
                return None
            fetched += data['result'][endpoint][query]['fetched']
            found = data['result'][endpoint][query]['found']
            items = OrderedDict(data['result'][endpoint][query]['items'])
            results.update(items)
            new_url = full_url + '&start=' + next(reversed(items))  # start next batch with last one from this batch
        return(results)


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--summary', type=str, help="Specify a domain for the Request Summary API")
    parser.add_argument('-d', '--domain', type=str, help="Specify a domain for the Domain API")
    parser.add_argument('-a', '--analytics', type=str, help="Specify a code for the Analytics API")
    parser.add_argument('-e', '--adsense', type=str, help="Specify a code for the Adsense API")
    parser.add_argument('-i', '--ipaddress', type=str, help="Specify an address for the IP Address API")
    parser.add_argument('-n', '--dns_domain', type=str, help="Specify a name for the Domains on Nameserver API")
    parser.add_argument('-p', '--ip_dns', type=str, help="Specify an address for the Nameservers on IP Address API")
    args, _ = parser.parse_known_args()

    pp = pprint.PrettyPrinter(indent=2)

    token = os.getenv("SPYONWEB_API")
    if not token:
        sys.stderr.write("Need API token in environment variable SPYONWEB_API\n")
        sys.exit()

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
