import pygame, os
from settings import *
from world_tile import WorldTile
from player import Player

class Game:
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()  

        # Create a surface for which all objects will be drawn onto. This surface is then scaled and drawn onto the main screen
        self.scaled_surface = pygame.Surface((screen_width / 2, screen_height / 2))

        # Attribute which is monitored by the game states controller
        self.running = False

        # --------------------------------------------------------------------------------------
        # Tile map
        self.tile_size = 32

        # Load the tile map images
        self.load_tile_map_images()

        # --------------------------------------------------------------------------------------
        # Camera
        self.players_spawning_point = [0, 0] # Stores the player's spawning point in the tile map
        self.last_tile_position = [0, 0] # Stores the position of the last tile in the tile 

    # --------------------------------------------------------------------------------------
    # Camera methods
    def update_camera_position(self):   

        # If the player has not traveled half of the size of the scaled screen width from their spawning position
        if self.players_spawning_point[0] <= self.player.rect.centerx < self.players_spawning_point[0] + (self.scaled_surface.get_width() / 2):
            # Don't move the camera
            camera_position_x = 0

        # If the player has traveled half of the size of the scaled screen width from their spawning position and is not half the width of the scaled screen from the last tile in the tile map
        elif (self.scaled_surface.get_width() / 2) < self.player.rect.centerx < self.last_tile_position[0] - (self.scaled_surface.get_width() / 2):
            # Set the camera to always follow the player
            camera_position_x = self.player.rect.centerx - (self.scaled_surface.get_width() / 2)

        # If the player is half the scaled screen width from the last tile in the tile map
        elif self.player.rect.centerx > self.last_tile_position[0] - (self.scaled_surface.get_width() / 2):
            # Set the camera to stop moving and be locked at half the size of the scaled screen width from the last tile in the tile map
            camera_position_x = self.last_tile_position[0] - self.scaled_surface.get_width() 
        
        # Update the camera position
        """
        - The camera's x position:
            - Starts at 0 until the player reaches half the size of the scaled screen width from the player's spawning position
            - Once the player reaches the center of the screen, then the camera will always follow the player
            - Until the player reaches half the size of the scaled screen width from the last tile in the tile map
        - The camera's y position 
            - Will always be the player's rect position minus half the size of the scaled screen height """
        self.camera_position = [camera_position_x, self.player.rect.y - (self.scaled_surface.get_height() / 2)]

    # --------------------------------------------------------------------------------------
    # Tile map methods
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

                        # Set the player as an attribute
                        self.player = player    

                        # Set the attribute of the player's spawning point to where the player was placed inside the tile map, this is for the camera effect
                        self.players_spawning_point = [self.player.rect.x, self.player.rect.y]

                    # World tile 1
                    case 2:
                        # Create a world tile
                        world_tile = WorldTile(x = (column_index * self.tile_size), y = (row_index * self.tile_size), image = pygame.transform.smoothscale(self.tile_images[1], (self.tile_size, self.tile_size)) )

                        # Add it to the list of all tile map objects
                        self.all_tile_map_objects.append(world_tile)

                        # Save the last tile position so that we can update the camera and limit the player's movement
                        self.last_tile_position = [column_index * self.tile_size, row_index * self.tile_size]

                        # Pass this position to the player class so that we can limit the player movement
                        self.player.last_tile_position = self.last_tile_position

    def draw_tile_map_objects(self):

        # For all tile objects in the level
        for tile_object in self.all_tile_map_objects:
            
            # if self.player.rect.x - 250 <= tile_object.rect.x <= self.player.rect.x + 250:

            # Draw the tile object at the camera position
            tile_object.draw(surface = self.scaled_surface, x = (tile_object.rect.x - self.camera_position[0]), y = (tile_object.rect.y - self.camera_position[1]))
    
    def run(self):
        
        # Fill the scaled surface with a colour
        self.scaled_surface.fill("white")

        # Update the camera position 
        self.update_camera_position()

        # Draw all objects inside the tile map / level
        self.draw_tile_map_objects()

        # pygame.draw.line(self.scaled_surface, "red", (self.scaled_surface.get_width() / 2, 0), (self.scaled_surface.get_width() / 2, self.scaled_surface.get_height() /  2))

        # Run the player methods
        self.player.run()
        
        # Draw the scaled surface onto the screen
        self.screen.blit(pygame.transform.scale(self.scaled_surface, (screen_width, screen_height)), (0, 0))