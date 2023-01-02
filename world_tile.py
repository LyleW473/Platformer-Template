import pygame
from objects import Object

class WorldTile(Object):
    def __init__(self, x, y, image):

        # Inherit from the objects class, which has the basic attributes and methods of all objects
        super().__init__(x = x, y = y, image = image)