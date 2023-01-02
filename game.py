import pygame
from settings import *

class Game:
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()  

        # Attribute which is monitored by the game states controller
        self.running = False

    def run(self):
        
        # Fill the screen with a colour
        self.screen.fill("dodgerblue4")