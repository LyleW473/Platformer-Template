import pygame, os
from settings import *
from world_tile import WorldTile
from player import Player

class Game:
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()  

        # Attribute which is monitored by the game states controller
        self.running = False
        # --------------------------------------------------------s------------------------------
        # Tile map
        self.tile_size = 32

        # Load the tile map images
        self.load_tile_map_images()

    def load_tile_map_images(self):

        # Create a dictionary filled with all of the tiles' images
        # Note: Start at index 1 because the "0" tile represents nothing. 
        self.tile_images = {i + 1: pygame.image.load(f"graphics/Tiles/{i + 1}.png").convert() for i in range(0, len(os.listdir("graphics/Tiles")))} 

    def create_objects_tile_map(self, non_transformed_tile_map):
        # Note: The objects tile map is created by the gamestates controller within the load_level method

        # Create an attribute which will hold all of the objects in the tile map
        self.all_tile_map_objects = []

        # For all rows of objects in the tile map
        for row_index, row in enumerate(non_transformed_tile_map):
            # For each item in each row
            for column_index, tile_map_object in enumerate(row):

                # Identify the tile map object
                match tile_map_object:

                    # Player
                    case 1:
                        # Create the player
                        player = Player(x = (column_index * self.tile_size), y = (row_index * self.tile_size))

                        # Add it to the list of all tile map objects
                        self.all_tile_map_objects.append(player)
        
                    # World tile 1
                    case 2:
                        # Create a world tile
                        world_tile = WorldTile(x = (column_index * self.tile_size), y = (row_index * self.tile_size), image = pygame.transform.smoothscale(self.tile_images[1], (self.tile_size, self.tile_size)) )

                        # Add it to the list of all tile map objects
                        self.all_tile_map_objects.append(world_tile)
        
    def draw_tile_map_objects(self):

        # For all tile objects in the level
        for tile_object in self.all_tile_map_objects:

            # Draw the tile
            tile_object.draw(self.screen)


    def run(self):
        
        # Fill the screen with a colour
        self.screen.fill("dodgerblue4")

        # Draw all objects inside the tile map / level
        self.draw_tile_map_objects()