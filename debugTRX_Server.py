import re

import TRX
from bottle import request
from bottle import route
from bottle import run
from spyonweb import Spyonweb

ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

# dispatcher


@route('/summary')
def summary():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        if (incoming.Type == "maltego.Domain" or incoming.Type == "maltego.DNSName") and re.match(ValidHostnameRegex, incoming.Value):
            s = Spyonweb(incoming.TransformSettings['api'])
            data = s.summary(incoming.Value)
            return process_summary(data)
        else:
            xform = TRX.MaltegoTransform()
            xform.addException("Must submit a valid host name or domain name")
            return xform.throwExceptions()


# process results into Maltego messages

def process_summary(data):
    xform = TRX.MaltegoTransform()
    if data['status'] != 'found':
        xform.addUIMessage("No results found", TRX.UIM_FATAL)
        return xform.returnOutput()
    name = data['result']['summary'].keys()[0]
    for code in data['result']['summary'][name]['items'].get('adsense', ''):
        ent = xform.addEntity("maltego.Phrase", code)
        ent.setWeight(data['result']['summary'][name]['items']['adsense'][code])
    for code in data['result']['summary'][name]['items'].get('analytics', ''):
        ent = xform.addEntity("maltego.Phrase", code)
        ent.setWeight(data['result']['summary'][name]['items']['analytics'][code])
    for server in data['result']['summary'][name]['items'].get('dns_servers', ''):
        ent = xform.addEntity("maltego.NSRecord", server)
        ent.setWeight(data['result']['summary'][name]['items']['dns_servers'][server])
    for ip in data['result']['summary'][name]['items'].get('ip', ''):
        ent = xform.addEntity("maltego.IPv4Address", ip)
        ent.setWeight(data['result']['summary'][name]['items']['ip'][ip])
    return xform.returnOutput()


# instantiate our class
# Start server
run(host='localhost', port=8192, debug=True, reloader=True)
