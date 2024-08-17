from pyproj import Transformer
import math

from_crs = "epsg:4326"
to_crs = "epsg:3405"

transformer = Transformer.from_crs(from_crs, to_crs, always_xy= True)
transformer_inverse = Transformer.from_crs(to_crs, from_crs, always_xy= True)

def convertLngLatToXY(lng, lat):
    return transformer.transform(lng, lat)

def convertXYToLatLng(x, y):
    return transformer_inverse.transform(x, y)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

