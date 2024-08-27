class Ponto:
    """A class that represents a certain point in the map at certain time"""
    def __init__(self,pointData):
        self.pointData = pointData

    def __str__(self):
        return self.pointData['Hora'] + " " + str(self.pointData['Coord'])