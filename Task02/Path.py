
class Path():
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f"lng: {self.lng}, lat: {self.lat}, RouteId: {self.RouteId}, RouteVarId: {self.RouteVarId}"

    #getter
    def getLat(self):
        return self.lat
    def getLng(self):
        return self.lng
    def getRouteId(self):
        return self.RouteId
    def getRouteVarId(self):
        return self.RouteVarId
    
    #setter
    def setLat(self, l):
        self.lat = l
    def setLng(self, l):
        self.lng = l
    def setRouteId(self, id):
        self.RouteId = id
    def setRouteVarId(self, id):
        self.RouteVarId = id