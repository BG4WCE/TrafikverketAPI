from TrafikverketAPI import generateRequest, getTrafficFlowData, getWeatherStationData
import xml.etree.ElementTree as ET
import requests
import json
import matplotlib.pyplot as plt
from osm import parser 
#import utm

def mapSite2Node(site, nodes, highways):
    # TODO: convert WGS-84 to UTM for distance calculation
    # TODO: set a threshold to check if the site is close enough to the node to avoid using wrong map
    dist_to_nodes = dict()
    for nodeId, nodePos in nodes.items():
        for way in highways:
            if nodeId in way[0]:
                dist = abs(nodePos[0]-site[0]) + abs(nodePos[1]-site[1])
                dist_to_nodes[nodeId] = dist
                break
            else:
                pass
    
    closestNode = (min(dist_to_nodes, key=dist_to_nodes.get))
    return {closestNode: dist_to_nodes[closestNode]}

def mapNode2Road(node, ways):
    # TODO: use the name in relation instead of way
    roadName = {'name':[], 'ref':[]}
    iWay = 0
    for way in ways:
        iWay = iWay + 1
        nodeList = way[0]
        print(iWay,': ', nodeList)
        if node in nodeList:
            print(iWay,': ', node, 'is in ', nodeList)
            if 'name' in way[1]:
                if 'ref' in way[1]:
                    roadName['ref'] = way[1].get('ref')
                else:
                    roadName['name'] = way[1].get('name')
            else:
                if roadName['name'] == []:
                    roadName['name'] ='no_name_way' 
        else:
            pass
            #print(node, 'is not in ', nodeList)
    
    return roadName

#reqType = 1  # WeatherStation
reqType = 2 # TrafficFlow
condition = str(14)

trafikverket_api = "https://api.trafikinfo.trafikverket.se/v2/data.json"
header = {'Content-Type': 'application/xml'} 
developer_key = '492ae49a423e4513a9ee93e600e331b4'
req = generateRequest(developer_key, reqType, condition)

r = requests.post(trafikverket_api, data=ET.tostring(req), headers=header)
json_response = r.json().get('RESPONSE').get('RESULT')[0].get('TrafficFlow')
#print(json_response)
nWeatherStations = len(json_response)
#BBox = [10.960, 14.730, 57.126, 59.260]
backgroud = plt.imread("map_traffic_flow.png")
plt.figure(figsize = (6,8)) 
stationPositions_lat = []
stationPositions_lon = []
sites = {}
for m in json_response:
    siteId = m['SiteId']
    pos_text = m['Geometry']['WGS84'][7:-1]
    [lon_str, lat_str] = pos_text.split(' ', 2)
    lat_num = float(lat_str)
    lon_num = float(lon_str)
    stationPositions_lat.append(lat_num)
    stationPositions_lon.append(lon_num)
    del m['Geometry']
    del m['SiteId']
    sites[siteId] = (lon_num, lat_num, m)
#print("SiteIds: ", list(sites))
BBox = [min(stationPositions_lon), max(stationPositions_lon), min(stationPositions_lat), max(stationPositions_lat)]
print(BBox)
plt.scatter(stationPositions_lon, stationPositions_lat, zorder=1, alpha=0.2, c='b', s=5)
for k, v in sites.items():
    plt.text(v[0], v[1], k)
plt.xlim(BBox[0],BBox[1])
plt.ylim(BBox[2],BBox[3])
plt.imshow(backgroud, zorder=0, extent = BBox)
plt.show()

# map matching
parsed_osm = parser.load_parse_osmxy(r"E6_Lackareback_map.osm")
print(parsed_osm.keys())
print("n Ways: ", len(parsed_osm.get('ways')))
highways = []
road_type_set = set()
for way in parsed_osm.get('ways'):
    if 'highway' in way[1]:
        if way[1].get('highway') not in road_type_set:
            road_type_set.add(way[1].get('highway'))
        if way[1].get('highway') in ('motoryway'):  # TODO: add other types if needed ('trunk', 'motorway_link', 'motorway_junction')
            highways.append(way)

print(road_type_set)
#print(highways)
print("n highways: ", len(highways))
#print(parsed_osm.get('ways'))
#for siteId, siteInfo in sites.items():
#    closestNode = mapSite2Node(siteInfo, parsed_osm.get('nodes'))
    #print(closestNode)
#    roadName = mapNode2Road(closestNode, parsed_osm.get('ways'))
#    print(roadName)

siteInfo = sites.get(5467)
print(siteInfo)
closestNode = mapSite2Node(siteInfo, parsed_osm.get('nodes'), highways)
print('site 5467 has',' closestNode ', closestNode)
roadName = mapNode2Road(list(closestNode)[0], highways)
print(roadName)