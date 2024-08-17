
class Stop():
    """def __init__(self, id, code, name, type, zone, ward, address_no, street, support, status, lng, lat, search, routes, ) -> None:
        self.StopId = id
        self.Code = code
        self.Name = name
        self.StopType = type
        self.Zone = zone
        self.Ward = ward
        self.AddressNo = address_no
        self.Street = street
        self.SupportDisability = support
        self.Status = status
        self.Lng  = lng
        self.Lat = lat
        self.Search = search
        self.Routes = routes"""

    def __init__(self, RouteId, RouteVarId, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.RouteId = RouteId
        self.RouteVarId = RouteVarId

    def __str__(self) -> str:
        return (
            f"StopId: {self.StopId}, Code: {self.Code}, Name: {self.Name}, StopType: {self.StopType}, Zone: {self.Zone}"
            f"Ward: {self.Ward}, AddressNo: {self.AddressNo}, Street: {self.Street}, SupportDisability: {self.SupportDisability}"
            f"Status: {self.Status}, Lng: {self.Lng}, Lat: {self.Lat}, Search: {self.Search}, Routes: {self.Routes}"
            f"RouteId: {self.RouteId}, "
        )
    #getter:
    def getStopId(self):
        return self.StopId
    def getCode(self):
        return self.Code
    def getName(self):
        return self.Name
    def getStopType(self):
        return self.StopType
    def getZone(self):
        return self.Zone
    def getWard(self):
        return self.Ward
    def getAddressNo(self):
        return self.AddressNo
    def getStreet(self):
        return self.Street
    def getSupportDisability(self):
        return self.SupportDisability
    def getStatus(self):
        return self.Status
    def getLng(self):
        return self.Lng
    def getLat(self):
        return self.Lat
    def getZone(self):
        return self.Zone
    def getSearch(self):
        return self.Search
    def getRouteId(self):
        return self.RouteId
    def getRouteVarId(self):
        return self.RouteVarId
    
    #setter:
    def setStopId(self, id):
        self.StopId = id
    def setCode(self, code):
        self.Code = code
    def setName(self, name):
        self.Name = name
    def setStopType(self, type):
        self.StopType = type
    def setZone(self, zone):
        self.Zone = zone
    def setWard(self, ward):
        self.Ward = ward
    def setAddressNo(self, no):
        self.AddressNo = no
    def setStreet(self, street):
        self.Street = street
    def setSupportDisability(self, sup):
        self.SupportDisability = sup
    def setStatus(self, status):
        self.Status = status
    def setLng(self, lng):
        self.Lng = lng
    def setLat(self, lat):
        self.getLat = lat
    def setZone(self, zone):
        self.Zone = zone
    def setSearch(self, search):
        self.Search = search
    def setRouteId(self, id):
        self.RouteId = id
    def setRouteVarId(self, id):
        self.RouteVarId = id
    
    