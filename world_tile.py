import pygame
from generic import Generic

class WorldTile(Generic):
    def __init__(self, x, y, image):

        # Inherit from the Generic class, which has basic attributes and methods.
        super().__init__(x = x, y = y, image = image)