import pygame
from Global.generic import Generic
from Global.settings import *

class Player(Generic, pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        
        # Surface that the player is drawn onto
        self.surface = surface

        # ---------------------------------------------------------------------------------
        # Animations

        self.animation_list = []
        self.animation_index = 0 
        self.animation_cooldown = 3000 
        self.animation_frame_counter = 0

        # Animation loading
        for i in range(0, 1): 
            # Load the border animation images
            animation_image = pygame.image.load(f"graphics/Player/{i}.png").convert_alpha()
            # Append the animation image to the animations list
            self.animation_list.append(animation_image)

        # Inherit from the Generic class, which has basic attributes and methods.
        Generic.__init__(self, x = x, y = y, image = self.animation_list[0])

        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self) 

        # ---------------------------------------------------------------------------------
        # Movement 
        """
        self.delta_time = delta_time
        self.movement_distance = 200 * self.delta_time
        """
        # ---------------------------------------------------------------------------------
        # Collisions
        """
        self.actual_player_position = None : Actual position of the player when the camera position is subtracted from the player rect's position
        self.camera_position = None # Position of the camera. This is updated inside "Game"
        self.last_tile_position = None # Position of the last tile that the player can be on. This will be updated by "Game" when the level is created
        """

    def play_animation(self):
        
        # Increment the counter 
        self.animation_frame_counter += 200
    
        # Set the image to be this animation frame
        self.image = self.animation_list[self.animation_index]

        # If enough time has passed since the last frame was played or since the animation was reset
        if self.animation_frame_counter > self.animation_cooldown:

            # If the border animation index isn't at the end of the list 
            if (self.animation_index < len(self.animation_list) - 1 ):
                # Increment the index
                self.animation_index += 1

            # If the border animation index is at the end of the list
            else:
                # Reset the index
                self.animation_index = 0
        
        # Reset the animation frame counter
        self.animation_frame_counter = 0

        # Draw the player onto the main screen
        self.draw(surface = self.surface, x = (self.rect.x - self.camera_position[0]), y = (self.rect.y - self.camera_position[1]))

    # ---------------------------------------------------------------------------------
    # Movement

    def handle_player_movement(self):

        # The distance the player travels with each key press
        self.move_distance = int(200 * self.delta_time)

        # If the "a" key is pressed and moving left won't place the player off the screen
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left - self.move_distance > 0:
            # Move the player left
            self.rect.x -= self.handle_tile_collisions(movement_direction = ("x", "left"))


        # If the "a" key is pressed and the player isn't at the end of the tile map
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.right + self.move_distance < self.last_tile_position[0]:
            # Move the player right
            self.rect.x += self.handle_tile_collisions(movement_direction = ("x", "right"))


        # If the "w" key is pressed
        if pygame.key.get_pressed()[pygame.K_w]:
            # Move the player up
            self.rect.y -= self.handle_tile_collisions(movement_direction = ("y", "up"))

        # If the "s" key is pressed
        if pygame.key.get_pressed()[pygame.K_s]:
            # Move the player down
            self.rect.y += self.handle_tile_collisions(movement_direction = ("y", "down"))

        pygame.draw.line(self.surface, "white", (self.surface.get_width() / 2, 0), (self.surface.get_width() / 2, self.surface.get_height()))

    def handle_tile_collisions(self, movement_direction):
    
        """ 
        Create a list containing the positions of the actual rectangle of the player according to how its seen on screen. The items are: x, y, top, bottom, left, right:

        - x = Found by subtracting how far the camera has traveled from the the player's rect x position
        - y = Found by subtracting how far the camera has traveled from the player's rect y position
        - Top = Same as y
        - Bottom = Top + the height of the player image
        - Left = Same as x 
        - Right = Left + the width of the player image
        
        self.actual_player_position = [
                                            self.rect.x - (self.camera_position[0]),
                                            self.rect.y - (self.camera_position[1]), 
                                            self.rect.y - (self.camera_position[1]),
                                            self.rect.y + self.image.get_height(),
                                            self.rect.x - (self.camera_position[0]),
                                            (self.rect.x - (self.camera_position[0])) + self.image.get_width()
                                            
                                            ]      

        The list above is the same as the list below:
        """ 
        # (x and left), (y and top), bottom, right
        self.actual_player_position = [
                                            self.rect.x - (self.camera_position[0]),
                                            self.rect.y - (self.camera_position[1]), 
                                            self.rect.y + self.image.get_height(),
                                            (self.rect.x - (self.camera_position[0])) + self.image.get_width()
                                            ]            
        # For each world tile
        for tile in self.world_tiles_group:

            # Create a new tile rect, which is a rectangle which holds the rectangle positions of the tile as it is being seen on screen
            camera_tile_rect = pygame.Rect(tile.rect.x - self.camera_position[0], tile.rect.y - self.camera_position[1], 32, 32)
    
            # If the player is trying to move along the x axis
            if movement_direction[0] == "x":
                
                # Left side of the player colliding with the right side of the tile
                if camera_tile_rect.colliderect(self.actual_player_position[0] - self.move_distance, self.actual_player_position[1], self.image.get_width(), self.image.get_height()):
                    
                    # Testing highlight
                    pygame.draw.rect(self.surface, "blue", camera_tile_rect, 0)
                    
                    # If the player is trying to move left
                    if movement_direction[1] == "left":
                        # Move the player as much to the left as we can before they collide with the tile
                        return self.move_distance - (camera_tile_rect.right - (self.actual_player_position[0] - self.move_distance))

                    # If the player is trying to move right
                    elif movement_direction[1] == "right":
                        # Let the player move right by the default move distance
                        return self.move_distance
              
                # Right side of the player colliding with the left side of the tile
                elif camera_tile_rect.colliderect(self.actual_player_position[0] + self.move_distance, self.actual_player_position[1], self.image.get_width(), self.image.get_height()):       
                    
                    pygame.draw.rect(self.surface, "blue", camera_tile_rect, 0)
                    
                    # If the player is trying to move left
                    if movement_direction[1] == "left":
                        # Let the player move left by the default move distance
                        return self.move_distance
                    
                    elif movement_direction[1] == "right":
                        # Move the player as much as to the right as we can before they collide with the tile
                        return self.move_distance - ((self.actual_player_position[3] + self.move_distance) - camera_tile_rect.left)

            # If the player is trying to move along the y axis
            elif movement_direction[0] == "y":

                # Testing phase
                return self.move_distance

        # If it still hasn't exited the method by now, then the player must not be colliding with anything
        return self.move_distance

    def run(self):
        
        # Testing rect
        #pygame.draw.rect(self.surface, "blue", self.rect, 0)

        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()

        # # Create / update a mask for pixel - perfect collisions (Uncomment later when adding collisions with objects other than tiles)
        # self.mask = pygame.mask.from_surface(self.image)