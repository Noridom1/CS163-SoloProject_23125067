from Path import *
import json
import csv

class PathQuery():
    Paths = []

    def __init__(self, PathsList = None) -> None:
        if PathsList == None:
            return
        self.Paths = PathsList

    def load_data(self, filename):
        with open(filename, 'r', encoding= 'utf8') as f:
            for line in f:
                data = json.loads(line.strip())
                self.Paths.append(Path(**data))

    def searchByRouteId(self, id):
        return [path for path in self.Paths if path.getRouteId() == id]
    def searchByRouteVarId(self, id):
        return [path for path in self.Paths if path.getRouteVarId() == id]
    def searchByRouteLat(self, lat):
        return [path for path in self.Paths if path.getLat() == lat]
    def searchByLng(self, lng):
        return [path for path in self.Paths if path.getLng() == lng]

    def outputAsCSV(self, result, filename):
        if result == None:
            return
        fields = result[0].__dict__.keys()
        with open(filename, 'w', encoding= 'utf8', newline='') as csvfile:
            writter = csv.DictWriter(csvfile, fieldnames= fields)
            writter.writeheader()
            for data in result:
                writter.writerow(data.__dict__)

    def outputAsJSON(self, result, filename):
        if result == None:
            return
        with open(filename, 'w', encoding= 'utf8') as jsonfile:
            for data in result:
                json.dump(data.__dict__, jsonfile, ensure_ascii= False)
                jsonfile.write("\n")