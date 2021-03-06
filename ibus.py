import requests
from bs4 import BeautifulSoup
import json
import re

def getSimilarStations(sn):
    url = "http://bus.2500.tv/station.php"
    response = requests.get(url, params={
        "station": sn
    })
    responseSoup = BeautifulSoup(response.text, "html.parser")
    dls = responseSoup.findAll("dl", attrs={
        "class": [
            "line",
            "fix"
        ]
    })
    stationMap = {}
    for dl in dls:
        link = dl.a.attrs['href']
        stationID = re.findall(r"stationID=([0-9]+)&", link)[0]
        _sn = dl.b.text.strip()
        ps = dl.findAll("p")
        location = ps[1].text
        if _sn in stationMap.keys():
            stationMap[_sn].append({location: {"stationID": stationID}})
        else:
            stationMap[_sn] = [{location: {"stationID": stationID}}]
    return json.dumps(stationMap)

def getBusInfoFormSN(sn, sid):
    url = "http://bus.2500.tv/stationList.php"
    reponse = requests.get(url, params={
        "name": sn,
        "stationID": sid
    })
    reponseSoup = BeautifulSoup(reponse.text, "html.parser")
    dls = reponseSoup.findAll("dl", attrs={
        "class": ["fix", "stationList"]
    })
    busInfos = []
    for dl in dls:
        ps = dl.findAll("p")
        busName = ps[0].b.text
        status = ps[0].span.text
        terminal = ps[1].text
        busInfos.append(
            {
                "busName": busName,
                "status": status,
                "terminal": terminal
            }
        )
    return json.dumps(busInfos)

def getLineList(lineName):
    url = "http://bus.2500.tv/line.php"
    response  = requests.get(url, params={
        'line': lineName
    })
    responseSoup = BeautifulSoup(response.text, 'html.parser')
    dls = responseSoup.find_all('dl', attrs={
        'class': [
            'fix', 'stationList'
        ]
    })
    lineList = []
    for dl in dls:
        lineID = dl.a.attrs['lineid']
        lineName = dl.b.text
        lineDire = dl.findAll('p')[1].text.strip()
        lineList.append({
            'lineID': lineID,
            'lineName': lineName,
            'lineDire': lineDire
        })
    return json.dumps(lineList)

def getBusStatus(lineID):
    url = 'http://bus.2500.tv/api_line_status.php'
    response = requests.post(url, data={
        'lineID': lineID
    })
    return response.content.replace(b'\xef',b'\x20').replace(b'\xbb', b'\x20').replace(b'\xbf', b'\x20').decode()

