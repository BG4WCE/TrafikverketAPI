'''Python interface for Trafikverket API
'''
import requests
import argparse
import xml.etree.ElementTree as ET
import json

def getTrafficFlowData(req, countyNo):
    # request traffic flow information
    query = ET.SubElement(req, 'QUERY', {'objecttype':"TrafficFlow", 'schemaversion':"1.4"})
    my_fileter = ET.SubElement(query, 'FILTER')
    ET.SubElement(my_fileter, 'EQ', {'name':"CountyNo", 'value':countyNo})
    include1 = ET.SubElement(query, 'INCLUDE')
    include1.text = 'AverageVehicleSpeed'
    include2 = ET.SubElement(query, 'INCLUDE')
    include2.text = 'MeasurementTime'
    include3 = ET.SubElement(query, 'INCLUDE')
    include3.text = 'MeasurementOrCalculationPeriod'
    include4 = ET.SubElement(query, 'INCLUDE')
    include4.text = 'SiteId'
    include5 = ET.SubElement(query, 'INCLUDE')
    include5.text = 'Geometry.WGS84'
    include6 = ET.SubElement(query, 'INCLUDE')
    include6.text = 'MeasurementSide'
    include7 = ET.SubElement(query, 'INCLUDE')
    include7.text = 'SpecificLane'
    include8 = ET.SubElement(query, 'INCLUDE')
    include8.text = 'VehicleFlowRate'
    ET.dump(req)
    return req

def getWeatherStationData(req, countyNo):
    # request weather station data
    query = ET.SubElement(req, 'QUERY', {'objecttype':"WeatherStation", 'schemaversion':"1"})
    my_fileter = ET.SubElement(query, 'FILTER')
    ET.SubElement(my_fileter, 'EQ', {'name':"CountyNo", 'value':countyNo})
    include1 = ET.SubElement(query, 'INCLUDE')
    include1.text = 'Measurement.Air.Temp'
    include2 = ET.SubElement(query, 'INCLUDE')
    include2.text = 'Measurement.MeasureTime'
    include3 = ET.SubElement(query, 'INCLUDE')
    include3.text = 'RoadNumberNumeric'
    include4 = ET.SubElement(query, 'INCLUDE')
    include4.text = 'Name'
    include5 = ET.SubElement(query, 'INCLUDE')
    include5.text = 'Geometry.WGS84'
    ET.dump(req)
    return req

def generateRequest(developer_key, reqType, condition):
    req = ET.Element('REQUEST')
    ET.SubElement(req, 'LOGIN', {'authenticationkey':developer_key})
    if reqType == 1:
        return getWeatherStationData(req, condition)

    if reqType == 2:
        return getTrafficFlowData(req, condition)
    return 0

def init_arg_parser():
    parser = argparse.ArgumentParser(description='use trafikverket api to get traffic and road information')
    parser.add_argument('reqType', choices=range(1,3), type=int, nargs=1,
    help='the request type: 1 = weather, 2 = traffic_flow')
    parser.add_argument('--condition', dest='condition', choices=range(1,24), type=int, help='query filter')
    parser.add_argument('--method', dest='method', choices=['get', 'stream'], help='choose method of getting the data')
    return parser

def main():
    print("running main()")
    parser = init_arg_parser()
    args = parser.parse_args()
    reqType = args.reqType[0]
    condition = args.condition
    method = args.method

    trafikverket_api = "https://api.trafikinfo.trafikverket.se/v2/data.json"
    header = {'Content-Type': 'application/xml'} 
    developer_key = '492ae49a423e4513a9ee93e600e331b4'
    req = generateRequest(developer_key, reqType, str(condition))

    if method == 'get':
        r = requests.post(trafikverket_api, data=ET.tostring(req), headers=header)
        json_response = r.json().get('RESPONSE').get('RESULT')[0].get('WeatherStation')
        nWeatherStations = len(json_response)
        print("Number of Weather Stations: ", nWeatherStations)
        for m in json_response:
            pos_text = m['Geometry']['WGS84'][7:-1]
            [lat, lon] = pos_text.split(' ', 2)
            print(lat, lon)
    else:  # stream
        pass
    
    
    
if __name__ == "__main__":
    main()