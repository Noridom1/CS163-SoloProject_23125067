from RouteVar import *
import json
import csv

class RouteVarQuery():
    RouteVars = []
    
    def __init__(self, RouteVarsList = None) -> None:
        if RouteVarsList == None:
            return
        self.RouteVars = RouteVarsList

    def load_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                route = json.loads(line.strip())
                for route_var in route:
                    self.RouteVars.append(
                        RouteVar(
                            route_var['RouteId'],
                            route_var["RouteVarId"],
                            route_var["RouteVarName"],
                            route_var["RouteVarShortName"],
                            route_var["RouteNo"],
                            route_var["StartStop"],
                            route_var["EndStop"],
                            route_var["Distance"],
                            route_var["Outbound"],
                            route_var["RunningTime"],
                            )
                        )

    def searchByRouteID(self, ID):
        return [route_var for route_var in self.RouteVars if route_var.getRouteId() == ID]
    
    def searchByRouteVarID(self, ID):
        return [route_var for route_var in self.RouteVars if route_var.getRouteVarId() == ID]

    def searchByRouteVarName(self, name):
        return [route_var for route_var in self.RouteVars if route_var.getRouteVarName() == name]
    
    def searchByRouteVarShortName(self, short_name):
        return [route_var for route_var in self.RouteVars if route_var.getRouteVarShortName() == short_name]
    
    def searchByRouteNo(self, no):
        return [route_var for route_var in self.RouteVars if route_var.getRouteNo() == no]
    
    def searchByStartStop(self, start):
        return [route_var for route_var in self.RouteVars if route_var.getStartStop() == start]
    
    def searchByEndStop(self, end):
        return [route_var for route_var in self.RouteVars if route_var.getEndStop() == end]
    
    def searchByDistance(self, dist):
        return [route_var for route_var in self.RouteVars if route_var.getDistance() == dist]
    
    def searchByOutbound(self, outbound):
        return [route_var for route_var in self.RouteVars if route_var.getOutbound() == outbound]
    
    def searchByRunningTime(self, running_time):
        return [route_var for route_var in self.RouteVars if route_var.getRunningTime() == running_time]
    
    def outputAsCSV(self, result, filename):
        fields = ['RouteId', 'RouteVarId', 'RouteVarName', 'RouteVarShortName', 'RouteNo', 
          'StartStop', 'EndStop', 'Distance', 'Outbound', 'RunningTime']
        with open(filename, 'w', encoding= "utf8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= fields)
            writer.writeheader()
            for data in result:
                writer.writerow(data.__dict__)

    def outputAsJSON(self, result, filename):
        with open(filename, 'w', encoding= 'utf8') as jsonfile:
            for data in result:
                json.dump(data.__dict__, jsonfile, ensure_ascii= False)
                jsonfile.write("\n")