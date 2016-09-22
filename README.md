# spyonweb

A Python library for the [Spyonweb API](https://api.spyonweb.com/v1/docs). Documentation for the RESTful API is available at https://api.spyonweb.com/v1/docs. NB: This Python library is not affiliated with Spyonweb.com. Be sure to review their [Terms of Service](http://www.spyonweb.com/terms).

## Available methods

- `summary`: The Request Summary API allows you to input a domain name and get the number of domains with the same Google Adsense, Google Analytics identifiers, IP Address, and Nameserver.
- `domain`: The Domain API allows you to input a domain and get a list of domains that share the same identifiers (Google Adsense, Google Analytics, IP Address, Nameserver).
- `adsense`: The Google Adsense API allows you to input a Google adsense identifier and get a list of domains that share the same identifier.
- `analytics`: The Google Analytics API allows you to input a Google Analytics identifier and get a list of domains that share the same identifier.
- `ipaddress`: The IP Address API allows you to input an IP address and get a list of domains hosted on this IP address.
- `dns_domain`: The Domains on Nameserver API allows you to input a nameserver and get a list of domains handled by this nameserver.
- `dns_ip`: The Nameservers on IP Address API allows you to input an IP address and get a list of nameservers using this IP address.

## Usage

```
import spyonweb


s = spyonweb.spyonweb(token=MY_TOKEN)
test_domain = "fullmooncalendar.net"

s.summary(test_domain)
```

returns

```
{
    "status": "found",
    "result": {
        "summary": {
            "fullmooncalendar.net": {
                "items": {
                    "adsense": {
                        // Format: "adsense_code": number_of_domains
                        "pub-5953444431482912": 10,
                        "pub-8423794689684356": 36
                    },
                    "analytics": {
                        // Format: "analytics_code": number_of_domains
                        "UA-15207196": 31,
                        "UA-34505845": 9
                    },
                    "dns_servers": {
                        // Format: "nameserver": number_of_domains
                        "erdomain.earth.orderbox-dns.com": 470,
                        "erdomain.mars.orderbox-dns.com": 470,
                        "erdomain.mercury.orderbox-dns.com": 469,
                        "erdomain.venus.orderbox-dns.com": 469
                    },
                    "ip": {
                        // Format: "ip_address": number_of_domains
                        "209.40.194.244": 9
                    }
                }
            }
        }
    }
}
```
