import pygame, os
from Global.settings import *
from Level.world_tile import WorldTile
from Level.player import Player

class Game:
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()  

        # Create a surface for which all objects will be drawn onto. This surface is then scaled and drawn onto the main screen
        self.scaled_surface = pygame.Surface((screen_width / 2, screen_height / 2))

        # Attribute which is monitored by the game states controller
        self.running = False

        # Delta time attribute is created
        # self.delta_time = None

        # --------------------------------------------------------------------------------------
        # Tile map
        self.tile_size = 32

        # Load the tile map images
        self.load_tile_map_images()

        # --------------------------------------------------------------------------------------
        # Camera
        self.last_tile_position = [0, 0] # Stores the position of the last tile in the tile (This is changed inside the create_objects_tile_map method)

        # Camera modes
        self.camera_mode = None # Can either be: Static, Follow

        # --------------------------------------------------------------------------------------
        # Groups
        self.all_tile_map_objects_group = pygame.sprite.Group()
        self.world_tiles_group = pygame.sprite.Group()
        # self.player_group = pygame.sprite.GroupSingle(self.player) This was created inside the create_objects_tile_map method

    # --------------------------------------------------------------------------------------
    # Misc methods

    def update_objects_delta_time(self, delta_time):
        # Used to update the delta time attributes of all objects within the tile map

        # For all objects
        for tile_map_object in self.all_tile_map_objects_group:
            # Update the object's delta time
            tile_map_object.delta_time = delta_time

    # --------------------------------------------------------------------------------------
    # Camera methods

    def set_camera_mode(self):
        # Used to change the camera mode depending on the size of the tile map
        
        # If the width of the tile map is one room
        if self.last_tile_position[0] <= (screen_width / 2):
            # Set the camera mode to "Static"
            self.camera_mode = "Static"
        
        # If the width of the tile map is more than one room
        else:
            # Set the camera mode to "Follow"
            self.camera_mode = "Follow"

    def update_camera_position(self):   
        # Moves the camera's position depending on what mode the camera has been set tow
        
        # If the camera mode is set to "Follow"
        if self.camera_mode == "Follow":

            # If the player is in half the width of the scaled screen from the first tile in the tile map
            if 0 <= self.player.rect.centerx <= (self.scaled_surface.get_width() / 2):
                # Don't move the camera
                camera_position_x = 0

            # If the player is in between half of the size of the scaled screen width from the first tile in the tile map and half the width of the scaled screen from the last tile in the tile map
            elif 0+ (self.scaled_surface.get_width() / 2) < self.player.rect.centerx < self.last_tile_position[0] - (self.scaled_surface.get_width() / 2):
                # Set the camera to always follow the player
                camera_position_x = self.player.rect.centerx - (self.scaled_surface.get_width() / 2)

            # If the player is half the scaled screen width away from the last tile in the tile mapsw
            elif self.player.rect.centerx >= self.last_tile_position[0] - (self.scaled_surface.get_width() / 2):
                # Set the camera to stop moving and be locked at half the size of the scaled screen width from the last tile in the tile map
                camera_position_x = self.last_tile_position[0] - self.scaled_surface.get_width() 

        # If the camera mode is set to "Static"
        elif self.camera_mode == "Static":
            # The camera's x position will always be at 0
            camera_position_x = 0
        
        # Update the camera position
        """
        - The camera's x position:
            - Starts at 0 until the player reaches half the size of the scaled screen width from the player's spawning position
            - Once the player reaches the center of the screen, then the camera will always follow the player
            - Until the player reaches half the size of the scaled screen width from the last tile in the tile map
        - The camera's y position 
            - Will always be at 0 """
        self.camera_position = [camera_position_x, 0]

        # Update the player's camera position attribute so that tile rects are correctly aligned
        self.player.camera_position = self.camera_position

    # --------------------------------------------------------------------------------------
    # Tile map methods

    def load_tile_map_images(self):

        # Create a dictionary filled with all of the tiles' images
        # Note: Start at index 1 because the "0" tile represents nothing. 
        self.tile_images = {i + 1: pygame.image.load(f"graphics/Tiles/{i + 1}.png").convert() for i in range(0, len(os.listdir("graphics/Tiles")))} 

    def create_objects_tile_map(self, non_transformed_tile_map):
        # Note: The objects tile map is created by the gamestates controller within the load_level method

        # For all rows of objects in the tile map
        for row_index, row in enumerate(non_transformed_tile_map):
            # For each item in each row
            for column_index, tile_map_object in enumerate(row):

                # Identify the tile map object
                match tile_map_object:

                    # Player
                    case 1:
                        # Create the player
                        self.player = Player(x = (column_index * self.tile_size), y = (row_index * self.tile_size), surface = self.scaled_surface)

                        # Add the player to its group
                        self.player_group = pygame.sprite.GroupSingle(self.player)

                        # Add the player to the group of all tile map objects
                        self.all_tile_map_objects_group.add(self.player)

                    # World tile 1
                    case 2:
                        # Create a world tile
                        world_tile = WorldTile(x = (column_index * self.tile_size), y = (row_index * self.tile_size), image = pygame.transform.smoothscale(self.tile_images[1], (self.tile_size, self.tile_size)))

                        # Add the world tile to its group
                        self.world_tiles_group.add(world_tile)

                        # Add it to the group of all tile map objects
                        self.all_tile_map_objects_group.add(world_tile)

        # Save the last tile position so that we can update the camera and limit the player's movement
        self.last_tile_position = [len(non_transformed_tile_map[0]) * self.tile_size, len(non_transformed_tile_map) * self.tile_size]
        self.player.last_tile_position = self.last_tile_position

        # Transfer the world tiles group to the player so that we can detect collisions within the Player class
        self.player.world_tiles_group = self.world_tiles_group

        # Set the camera mode 
        self.set_camera_mode()

    def draw_tile_map_objects(self):

        # Calls the draw methods of all objects in the level

        # ---------------------------------------------
        # World tiles

        for world_tile in self.world_tiles_group:

            #world_tile.draw(surface = self.scaled_surface, x = world_tile.rect.x , y = world_tile.rect.y )

            # Check the x co-ordinate of the camera
            match self.camera_position[0]:
                 
                # If the camera is positioned at the start of the tile map and the object is within the boundaries of the screen
                case 0 if world_tile.rect.x <= self.scaled_surface.get_width():

                    # Draw all tile objects on the screen
                    world_tile.draw(surface = self.scaled_surface, x = (world_tile.rect.x - self.camera_position[0]), y = (world_tile.rect.y - self.camera_position[1]))

                # If the camera is positioned at the end of the tile map and the tile object is within the boundaries of the screen
                case _ if (self.last_tile_position[0] - self.scaled_surface.get_width()) == self.camera_position[0] and world_tile.rect.x >= self.camera_position[0]:

                    # Draw all tile objects on the screen
                    world_tile.draw(surface = self.scaled_surface, x = (world_tile.rect.x - self.camera_position[0]), y = (world_tile.rect.y - self.camera_position[1]))

                # If the camera is neither at the start or the end of the tile map and the object is within the boundaries of the screen
                case _ if self.player.rect.left - ((self.scaled_surface.get_width() / 2) + self.tile_size)  <= world_tile.rect.x <= self.player.rect.right + (self.scaled_surface.get_width() / 2): 

                    # Draw the tile object at the camera position
                    world_tile.draw(surface = self.scaled_surface, x = (world_tile.rect.x - self.camera_position[0]), y = (world_tile.rect.y - self.camera_position[1]))

    def handle_collisions(self):
        
        # Save for later (for enemies, etc.)
        # # --------------------------------------------------------------------------------------
        # # Look for a slightly less accurate collision check between the tile and the player sprite
        # if pygame.sprite.spritecollide(self, self.world_tiles_group, False):

        #     # Create a list of all the tiles that the player collided (more accurate collision check)
        #     if pygame.sprite.spritecollide(self, self.world_tiles_group, False, pygame.sprite.collide_mask):
        pass

    # --------------------------------------------------------------------------------------
    # Gameplay methods

    def run(self, delta_time):

        # Update the delta time of all objects 
        self.update_objects_delta_time(delta_time)
        
        # Fill the scaled surface with a colour
        self.scaled_surface.fill("dodgerblue4")

        # Update the camera position 
        self.update_camera_position()

        # Draw all objects inside the tile map / level
        self.draw_tile_map_objects()

        # # Handle collisions between all objects in the level
        # self.handle_collisions()

        # Run the player methods
        self.player.run()

        # Draw the scaled surface onto the screen
        self.screen.blit(pygame.transform.scale(self.scaled_surface, (screen_width, screen_height)), (0, 0))