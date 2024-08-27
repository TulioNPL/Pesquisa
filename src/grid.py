from collections import defaultdict
from ponto import Ponto
import re 


class Grid:

    def __init__(self):
        self.grid = defaultdict(list)
        self.latituderef = 0
        self.longituderef = 0
        self.fator = 0
        self.numberOfPoints = 0
    
    def clear(self):
        self.grid.clear()

    #add point to grid
    def add_point(self, point):
        Lat = int(self.get_lat_point_projecao(point) * self.fator)
        Long = int(self.get_long_point_projecao(point) * self.fator)
        self.grid[(Lat,Long)].append(point)
        self.numberOfPoints += 1
    
    #add point to grid
    def add_point_duration(self, point):
        Lat = int(self.get_lat_point_projecao(point) * self.fator)
        Long = int(self.get_long_point_projecao(point) * self.fator)
        self.grid[(Lat,Long)].append(point)
        self.numberOfPoints += 1
    
    #add point meters
    def add_point_meters(self, point):
        Lat = int(self.get_lat_point_projecao_meters(point) / self.fator)
        Long = int(self.get_long_point_projecao_meters(point) / self.fator)
        self.grid[(Lat,Long)].append(point)
        self.numberOfPoints += 1

    #latitude point reference
    def get_lat_point_projecao(self, point):
        projecaoLat = Point(0, float(point.X), self.longituderef, 0)
        cellLat = self.pointRef.distance_gps_to(projecaoLat)
        return cellLat
    
    #longitude point reference
    def get_long_point_projecao(self, point):
        projecaoLong = Point(0, self.latituderef, float(point.Y), 0)
        cellLong = self.pointRef.distance_gps_to(projecaoLong)
        return cellLong

    #latitude point reference
    def get_lat_point_projecao_meters(self, point):
        projecaoLat = Point(0, float(point.X), self.longituderef, 0)
        cellLat = self.pointRef.distance(projecaoLat)
        return cellLat
    
    #longitude point reference
    def get_long_point_projecao_meters(self, point):
        projecaoLong = Point(0, self.latituderef, float(point.Y), 0)
        cellLong = self.pointRef.distance(projecaoLong)
        return cellLong

    #get my_points
    def get_points(self):
        allPoints = []
        for points in self.grid.itervalues():
            allPoints.extend(points)
        return allPoints

    #amount of points added
    def get_number_of_points(self):
        return self.numberOfPoints
    
    #get point neighborhood
    def get_neighborhood_points(self, point):
        list_points = []
        Lat = int(self.get_lat_point_projecao(point) * self.fator)
        Long = int(self.get_long_point_projecao(point) * self.fator)
    
        list_points.extend(self.grid[(Lat-1,Long-1)])
        list_points.extend(self.grid[(Lat-1,Long)])
        list_points.extend(self.grid[(Lat-1,Long+1)])
        list_points.extend(self.grid[(Lat,Long-1)])
        list_points.extend(self.grid[(Lat,Long)])
        list_points.extend(self.grid[(Lat,Long+1)])
        list_points.extend(self.grid[(Lat+1,Long-1)])
        list_points.extend(self.grid[(Lat+1,Long)])
        list_points.extend(self.grid[(Lat+1,Long+1)])
        return list_points

    #get point neighborhood meters (trace colgone)
    def get_neighborhood_points_meters(self, point):
        list_points = []
        Lat = int(self.get_lat_point_projecao_meters(point) / self.fator)
        Long = int(self.get_long_point_projecao_meters(point) / self.fator)
    
        list_points.extend(self.grid[(Lat-1,Long-1)])
        list_points.extend(self.grid[(Lat-1,Long)])
        list_points.extend(self.grid[(Lat-1,Long+1)])
        list_points.extend(self.grid[(Lat,Long-1)])
        list_points.extend(self.grid[(Lat,Long)])
        list_points.extend(self.grid[(Lat,Long+1)])
        list_points.extend(self.grid[(Lat+1,Long-1)])
        list_points.extend(self.grid[(Lat+1,Long)])
        list_points.extend(self.grid[(Lat+1,Long+1)])
        return list_points