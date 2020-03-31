from TrafikverketAPI import generateRequest, getTrafficFlowData, getWeatherStationData
import xml.etree.ElementTree as ET
import requests
import json
import matplotlib.pyplot as plt

reqType = 1
condition = str(14)

trafikverket_api = "https://api.trafikinfo.trafikverket.se/v2/data.json"
header = {'Content-Type': 'application/xml'} 
developer_key = '492ae49a423e4513a9ee93e600e331b4'
req = generateRequest(developer_key, reqType, condition)

r = requests.post(trafikverket_api, data=ET.tostring(req), headers=header)
json_response = r.json().get('RESPONSE').get('RESULT')[0].get('WeatherStation')
nWeatherStations = len(json_response)
BBox = [10.960, 14.730, 57.126, 59.260]
backgroud = plt.imread("map_vastra_gotalands_lan.png")
plt.figure() #figsize = (17,12)
stationPositions_lat = []
stationPositions_lon = []
for m in json_response:
    pos_text = m['Geometry']['WGS84'][7:-1]
    [lon, lat] = pos_text.split(' ', 2)
    stationPositions_lat.append(float(lat))
    stationPositions_lon.append(float(lon))
#BBox = [min(stationPositions_lon), max(stationPositions_lon), min(stationPositions_lat), max(stationPositions_lat)]
plt.scatter(stationPositions_lon, stationPositions_lat, zorder=1, alpha=0.2, c='b', s=5)
plt.xlim(BBox[0],BBox[1])
plt.ylim(BBox[2],BBox[3])
plt.imshow(backgroud, zorder=0, extent = BBox)
plt.show()