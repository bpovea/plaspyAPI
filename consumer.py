import datetime
import urllib
import inspect
import settings_local
from datetime import timedelta
from urllib.request import Request

class PRequest:
    Account = settings_local.account
    ApiKey = settings_local.apiKey
    IdDevice = settings_local.idDevice
    LastPosition = True
    StartUTC = str(datetime.datetime.utcnow() - timedelta(hours=12))
    EndUTC = str(datetime.datetime.utcnow())
    def props(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                pr[name] = value
        return pr
    def GetParamsRequest(self):
        return urllib.parse.urlencode(self.props())
    def GetXMLRequest(self):
        request="<PRequest>"
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                request+="<"+name +">" + str(value) + "</"+name +">"
        request+= "</PRequest>"
        return request

APIURL = "http://api.plaspy.com/api/GetLocation"
# APIURL = "https://api.plaspy.com/api/GetLocation"
request= PRequest()

print("Testing POST")
print("Request: " + request.GetParamsRequest())
f = urllib.request.urlopen(APIURL, request.GetParamsRequest().encode())
response= f.read()
print("Response: " + str(response))
print()
f.close()


print("Testing POST XML")
print("Request: " + request.GetXMLRequest())
q= Request(APIURL, request.GetXMLRequest().encode(), headers= {'Content-type': 'text/xml'})
f= urllib.request.urlopen(q)
response= f.read()
print("Response: " + str(response))
print()
f.close()


print("Testing POST JSON")
print("Request: " + str(request.props()))
q= Request(APIURL, str(request.props()).encode(), headers= {'Content-type': 'application/json'})
f= urllib.request.urlopen(q)
response= f.read()
print("Response: " + str(response))
print()
f.close()


print("Testing Get JSON")
print("Request: " + request.GetParamsRequest())
f = urllib.request.urlopen(APIURL + "?" + request.GetParamsRequest())
response= f.read()
print("Response: " + str(response))
print()
f.close()

