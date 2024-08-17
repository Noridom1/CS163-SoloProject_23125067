from Stop import *
import json
import csv

class StopQuery():
    Stops = []
    def __init__(self, StopsList = None) -> None:
        if StopsList == None:
            return
        self.Stops = StopsList
    
    def load_data(self, filename):
        with open(filename, 'r', encoding= 'utf8') as f:
            for line in f:
                data = json.loads(line.strip())
                for stop in data["Stops"]:
                    self.Stops.append(Stop(data["RouteId"], data["RouteVarId"],**stop))

    def searchByStopId(self, id):
        return [stop for stop in self.Stops if stop.getStopId() == id]
    
    def searchByCode(self, code):
        return [stop for stop in self.Stops if stop.getCode() == code]
    
    def searchByName(self, name):
        return [stop for stop in self.Stops if stop.getName() == name]
    
    def searchByStopType(self, type):
        return [stop for stop in self.Stops if stop.getZone() == type]
    
    def searchByZone(self, zone):
        return [stop for stop in self.Stops if stop.getZone() == zone]
    
    def searchByWard(self, ward):
        return [stop for stop in self.Stops if stop.getWard() == ward]
    
    def searchByAddressNo(self, no):
        return [stop for stop in self.Stops if stop.getAddressNo() == no]
    
    def searchByStreet(self, street):
        return [stop for stop in self.Stops if stop.getStreet() == street]
    
    def searchBySupportDisability(self, sup):
        return [stop for stop in self.Stops if stop.getSupportDisability() == sup]
    
    def searchByStatus(self, status):
        return [stop for stop in self.Stops if stop.getStatus() == status]
    
    def searchByLng(self, lng):
        return [stop for stop in self.Stops if stop.getLng() == lng]
    
    def searchByLat(self, lat):
        return [stop for stop in self.Stops if stop.getLat() == lat]
    
    def searchBySearch(self, search):
        return [stop for stop in self.Stops if stop.getSearch() == search]
    
    def searchByRoutes(self,routes):
        return [stop for stop in self.Stops if stop.getRoutes() == routes]
    
    def searchByRouteId(self, id):
        return [stop for stop in self.Stops if stop.getRouteId() == id]
    
    def searchByRouteVarId(self, id):
        return [stop for stop in self.Stops if stop.getRouteVarId() == id]
    
    def outputAsCSV(self, result, filename):
        if result == None:
            return
        fields = result[0].__dict__.keys()
        with open(filename, 'w', encoding= 'utf8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= fields)
            writer.writeheader()
            for data in result:
                writer.writerow(data.__dict__)

    def outputAsJSON(self, result, filename):
        if result == None:
            return
        with open(filename, 'w', encoding= 'utf8') as jsonfile:
            for data in result:
                json.dump(data.__dict__, jsonfile, ensure_ascii= False)
                jsonfile.write("\n")