import logging
import os
import re

from bottle import request
from bottle import route
from bottle import run
from spyonweb import spyonweb
from TRX import TRX

ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidAdsenseRegex = "^pub-[0-9]+$"
ValidAnalyticsRegex = "^UA-[0-9]+$"

# dispatcher


@route('/summary', method='POST')
def summary():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        if (incoming.Type == "Domain" or incoming.Type == "DNSName") and re.match(ValidHostnameRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.summary(incoming.Value)
                return process_summary(data)
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform = TRX.MaltegoTransform()
            xform.addException("Must submit a valid host name or domain name")
            return xform.throwExceptions()


@route('/domain', method='POST')
def domain():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        if (incoming.Type == "Domain" or incoming.Type == "DNSName") and re.match(ValidHostnameRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.domain(incoming.Value)
                return process_domain(data)
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform = TRX.MaltegoTransform()
            xform.addException("Must submit a valid host name or domain name")
            return xform.throwExceptions()


@route('/adsense', method='POST')
def adsense():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        xform = TRX.MaltegoTransform()
        if incoming.Type == "Phrase" and re.match(ValidAdsenseRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.adsense(incoming.Value, limit=incoming.Slider)
                if data['status'] != 'found':
                    xform.addUIMessage("No results found", TRX.UIM_FATAL)
                    return xform.returnOutput()
                for name in data:
                    ent = xform.addEntity("maltego.Domain", name)
                    ent.setLinkLabel(data[name])  # date ID was associated with domain
                return xform.returnOutput()
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform.addException("Must submit a valid Adsense publisher ID")
            return xform.throwExceptions()


@route('/analytics', method='POST')
def analytics():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        xform = TRX.MaltegoTransform()
        if incoming.Type == "Phrase" and re.match(ValidAnalyticsRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.analytics(incoming.Value, limit=incoming.Slider)
                if data['status'] != 'found':
                    xform.addUIMessage("No results found", TRX.UIM_FATAL)
                    return xform.returnOutput()
                for name in data:
                    ent = xform.addEntity("maltego.Domain", name)
                    ent.setLinkLabel(data[name])  # date ID was associated with domain
                return xform.returnOutput()
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform.addException("Must submit a valid Analytics tracking ID")
            return xform.throwExceptions()


@route('/ip', method='POST')
def ip():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        xform = TRX.MaltegoTransform()
        if re.match(ValidIpAddressRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.ipaddress(incoming.Value, limit=incoming.Slider)
                if data is None:
                    xform.addUIMessage("No results found", TRX.UIM_FATAL)
                    return xform.returnOutput()
                for name in data:
                    ent = xform.addEntity("maltego.Domain", name)
                    ent.setLinkLabel(data[name])  # date IP address was associated with domain
                return xform.returnOutput()
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform.addException("Must submit a valid IPv4 address")
            return xform.throwExceptions()


@route('/dns_domain', method='POST')
def dns_domain():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        xform = TRX.MaltegoTransform()
        if (incoming.Type == "Domain" or incoming.Type == "DNSName" or incoming.Type == "NSRecord") and re.match(ValidHostnameRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.dns_domain(incoming.Value, limit=incoming.Slider)
                if data['status'] != 'found':
                    xform.addUIMessage("No results found", TRX.UIM_FATAL)
                    return xform.returnOutput()
                for name in data:
                    ent = xform.addEntity("maltego.Domain", name)
                    ent.setLinkLabel(data[name])  # date domain name was associated with server
                return xform.returnOutput()
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform.addException("Must submit a valid host name")
            return xform.throwExceptions()


@route('/ip_dns', method='POST')
def ip_dns():
    if request.body.len > 0:
        incoming = TRX.MaltegoMsg(request.body.getvalue())
        xform = TRX.MaltegoTransform()
        if re.match(ValidIpAddressRegex, incoming.Value):
            if 'api' in incoming.TransformSettings:
                s = spyonweb.Spyonweb(incoming.TransformSettings['api'])
                data = s.ip_dns(incoming.Value, limit=incoming.Slider)
                if data['status'] != 'found':
                    xform.addUIMessage("No results found", TRX.UIM_FATAL)
                    return xform.returnOutput()
                for name in data:
                    ent = xform.addEntity("maltego.NSRecord", name)
                    ent.setLinkLabel(data[name])  # date domain name was associated with server
                return xform.returnOutput()
            else:
                xform = TRX.MaltegoTransform()
                xform.addException("Must submit an API key")
                return xform.throwExceptions()
        else:
            xform.addException("Must submit a valid IP address")
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


def process_domain(data):
    xform = TRX.MaltegoTransform()
    if data['status'] != 'found':
        xform.addUIMessage("No results found", TRX.UIM_FATAL)
        return xform.returnOutput()
    name = data['result']['domain'].keys()[0]
    for code in data['result']['domain'][name]['items'].get('adsense', ''):
        ent = xform.addEntity("maltego.Phrase", code)
        ent.setWeight(data['result']['domain'][name]['items']['adsense'][code])
    for code in data['result']['domain'][name]['items'].get('analytics', ''):
        ent = xform.addEntity("maltego.Phrase", code)
        ent.setWeight(data['result']['domain'][name]['items']['analytics'][code])
    for server in data['result']['domain'][name]['items'].get('dns_servers', ''):
        ent = xform.addEntity("maltego.NSRecord", server)
        # TODO: how to represent IP addresses returned in this API call?
    for ip in data['result']['domain'][name]['items'].get('ip', ''):
        ent = xform.addEntity("maltego.IPv4Address", ip)
        ent.setWeight(data['result']['domain'][name]['items']['ip'][ip])
    return xform.returnOutput()


# instantiate our class
# Start server
logging.basicConfig(filename='spyonweb-maltego.log', level=logging.DEBUG)
run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
