from typing import List


class PixelCluster():


    def __init__(self, coordinates:List):
        self.coordinates = coordinates
        self.length = len(coordinates)

    def __str__(self):
        return str(self.coordinates)
