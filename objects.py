import pygame

class Object:
    def __init__(self, x, y, image):

        # Image
        self.image = image

        # Get the rect from the image size
        self.rect = self.image.get_rect()

        # X and Y
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):

        # Draw the tile onto the surface
        surface.blit(self.image, self.rect)