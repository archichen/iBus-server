from flask import Flask, url_for, render_template
from ibus import getSimilarStations as getSimilarStations
from ibus import getBusInfoFormSN as getBusInfoFormSN
from ibus import getLineList as getLineList
from ibus import getBusStatus as getBusStatus

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/get_similar_stations/<stationName>')
def get_similar_stations(stationName):
    rep = getSimilarStations(stationName)
    return rep

@app.route('/get_businfo/<stationName>/<stationID>')
def get_busInfo(stationName, stationID):
    rep = getBusInfoFormSN(stationName, stationID)
    return rep

@app.route('/get_linelist/<lineName>')
def get_linelist(lineName):
    rep = getLineList(lineName)
    return rep

@app.route('/get_bustatus/<lineID>')
def get_bustatus(lineID):
    rep = getBusStatus(lineID)
    return rep

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
