import pyshark
import requests
import json
import sys

# return URI.
def geturi(cap,numberofpacket):
    http = str(cap[numberofpacket].http)
    pos_uri = http.split()
    uri = pos_uri[73]
    return uri

# return headers for POST request.
def getheaders(cap,numberofpacket):
    http = str(cap[numberofpacket].http)
    
    pos1 = http.find("Host:")
    pos2 = http.find("Content-Type:")
    host = http[pos1+6:pos2-6]

    pos1 = http.find("Cookie: TP_SESSIONID=")
    pos2 = http.find("Cookie pair:")
    cookie = http[pos1+21:pos2-6]

    pos1 = http.find("User-Agent: ")
    pos2 = http.find("Accept-Language")
    useragent = http[pos1+12:pos2-6]

    pos1 = http.find("Content-Length: ")
    contentlenght = http[pos1+16:pos1+19]

    header = {
        "Host":host,
        "Content-Type":"application/json;UTF-8",
        "Accept":"*/*",
        "Connection":"keep-alive",
        "Cookie":"TP_SESSIONID="+cookie,
        "User-Agent":useragent,
        "Accept-Language":"it-IT;q=1",
        "Content-Lenght":contentlenght
    }

    return header
    
# return JSON with inside securePassthrough method and the encrypted request.
def getjson(cap,numberofpacket):
    js = str(cap[numberofpacket].json)
    
    pos1 = js.find("/params/request:")
    pos1 = pos1 + 16
    pos2 = js.find("Member with value: request:")
    request = js[pos1:pos2-2]
    
    pos1 = js.find("Member with value: terminalUUID:")
    pos1 = pos1 + 32
    pos2 = js.find("String value: securePassthrough")
    uuid = js[pos1:pos2-2]

    secureData = {
        "method":"securePassthrough",
        "params":{
          "request": request
          },
        "terminalUUID": uuid
        }
    return json.dumps(secureData)

nome_script, nome_pcap, numero_pacchetto = sys.argv

# upload a pcap file 
cap = pyshark.FileCapture(nome_pcap)

# send a POST request with headers and json obtained.
response = requests.post(geturi(cap,int(numero_pacchetto)-1),data=getjson(cap,int(numero_pacchetto)-1), verify=False, headers = getheaders(cap,int(numero_pacchetto)-1))

#output HTTP response
print(response)
