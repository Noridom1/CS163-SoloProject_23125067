import json
from PathQuery import *

def generateGeoJsonPath(PathsList, RouteId = None, RouteVarId = None, lngs = None, lats = None):
    if lngs == None or lats == None:
        PathsListQuery = PathQuery(PathQuery(PathsList).searchByRouteId(str(RouteId))).searchByRouteVarId(str(RouteVarId))
        path = PathsListQuery[0]
        lngs = path.getLng()
        lats = path.getLat()
    # Ensure the lists have the same length
    assert len(lngs) == len(lats), "Longitude and latitude lists must be of the same length"

    # Create a list of features for the GeoJSON
    coordinates = []
    for lng, lat in zip(lngs, lats):
        coordinates.append([lng, lat])

    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {}
            }
        ]
    }

    # Write the GeoJSON to a file
    with open('path.geojson', 'w') as f:
        json.dump(geojson, f, indent=4)

    print("GeoJSON file 'path.geojson' created successfully.")

def generatePath(CoordinatesList, filename):
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": CoordinatesList
                },
                "properties": {}
            }
        ]
    }

    # Write the GeoJSON to a file
    with open(filename, 'w') as f:
        json.dump(geojson, f, indent=4)

    print(f"GeoJSON file {filename} created successfully.")

def generateGeoJsonPoints(StopsList, RouteId = None, RouteVarId = None, lngs = None, lats = None):
    PointsDict = {
        stop.getStopId() : [stop.getLng(), stop.getLat()]
        for stop in StopsList
    }
    features = []
    for coor in PointsDict.values():
        features.append(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "coordinates": coor,
                    "type": "Point"
                }
            },
        )
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('nodes.geojson', 'w') as f:
        json.dump(geojson, f, indent=4)

    print("GeoJSON file 'nodes.geojson' created successfully.")


    

