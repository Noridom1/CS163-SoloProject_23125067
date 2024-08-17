
class RouteVar():
    def __init__(self, route_id, route_var_id, route_var_name, route_var_short, route_no, start, end, dist, outbound, time):
        self.RouteId = route_id
        self.RouteVarId = route_var_id
        self.RouteVarName = route_var_name
        self.RouteVarShortName = route_var_short
        self.RouteNo = route_no
        self.StartStop = start
        self.EndStop = end
        self.Distance = dist
        self.Outbound = outbound
        self.RunningTime = time

    def __str__(self):
        return (f'"RouteId":{self.getRouteId()}, "RouteVarId":{self.getRouteVarId()}, "RouteVarName":{self.getRouteVarName()}, '
                f'"RouteVarShortName":{self.getRouteVarShortName()}, "RouteNo":{self.getRouteNo()}, "StartStop":{self.getStartStop()}, '
                f'"EndStop":{self.getEndStop()}, "Distance":{self.getDistance()}, "Outbound":{self.getOutbound()}, "RunningTime":{self.getRunningTime()}')

    def getRouteId(self):
        return self.RouteId
    
    def getRouteVarId(self):
        return self.RouteVarId
    
    def getRouteVarShortName(self):
        return self.RouteVarShortName
    
    def getRouteVarName(self):
        return self.RouteVarName
    
    def getRouteNo(self):
        return self.RouteNo
    
    def getStartStop(self):
        return self.StartStop
    
    def getEndStop(self):
        return self.EndStop
    
    def getDistance(self):
        return self.Distance
    
    def getOutbound(self):
        return self.Outbound
    
    def getRunningTime(self):
        return self.RunningTime
    
    def setRouteId(self, route_id):
        self.RouteId = route_id
    
    def setRouteVarId(self, route_var_id):
        self.RouteVarId = route_var_id
    
    def setRouteVarName(self, route_var_name):
        self.RouteVarName = route_var_name
    
    def setRouteVarShortName(self, route_var_short):
        self.RouteVarShortName = route_var_short

    def setRouteNo(self, route_no):
        self.RouteNo = route_no
    
    def setStartStop(self, start):
        self.StartStop = start
    
    def setEndStop(self, end):
        self.EndStop = end
    
    def setDistance(self, dist):
        self.Distance = dist
    
    def setOutbound(self, outbound):
        self.Outbound = outbound
    
    def setRunningTime(self, time):
        self.RunningTime = time