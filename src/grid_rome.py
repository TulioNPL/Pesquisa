from ponto import Ponto
from grid import Grid


# network modeling
# MaxX: 12.7864216809     MinX: 12.1712615993     MaxY: 42.2393299814     MinY 41.5660477042
class Grid_Rome(Grid):
    
    #init global values
    def __init__(self):
        Grid.__init__(self)
        pnt['Coord'] = (41.8899802396, 12.4899285294)
        self.pointRef = Ponto(pnt)
        self.latituderef = 41.8899802396
        self.longituderef = 12.4899285294
        self.numberOfPoints = 0
        self.fator = 100

