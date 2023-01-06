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
        self.movement_distance_x = 200 * self.delta_time
        self.move_distance_y = int(150 * self.delta_time)
        """
        # Jumping 
        self.jump_deceleration = 1
        self.gravity = 0
        self.head_and_tile_collided = False
        self.peak_jump_height_reached = False
        self.allowed_to_jump = True

        # ---------------------------------------------------------------------------------
        # Collisions
        """
        self.actual_player_position = None : Actual position of the player when the camera position is subtracted from the player rect's position
        self.camera_position = None # Position of the camera. This is updated inside "Game"
        self.last_tile_position = None # Position of the last tile that the player can be on. This will be updated by "Game" when the level is created
        """
        self.neighbouring_tiles_dict = {} # Used to hold the neighbouring tiles near the player (i.e. within 1 tile of the player, horizontally and vertically)

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

    def find_actual_player_position(self):

        # Used to find the actual position of the player according to where they are on-screen.

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
                                            self.rect.y - (self.camera_position[1]) + self.image.get_height(),
                                            self.rect.x - (self.camera_position[0]),
                                            (self.rect.x - (self.camera_position[0])) + self.image.get_width()
                                            
                                            ]      

        The list above is the same as the list below:
        """ 
        # (x and left), (y and top), bottom, right
        self.actual_player_position = [
                                            self.rect.x - self.camera_position[0],
                                            self.rect.y - self.camera_position[1], 
                                            (self.rect.y - self.camera_position[1]) + self.image.get_height(),
                                            (self.rect.x - self.camera_position[0]) + self.image.get_width()
                                            ]            

    def handle_gravity(self):

        # Increase the strength of gravity
        self.gravity += 30 * self.delta_time

        # Limit gravity to 80
        if self.gravity > 200:
            self.gravity = 200

        # Increase the player's y position by the amount it is allowed to move by
        self.rect.y += self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.gravity)

    def jump(self):

        # If the player isn't x tiles above where they started the jump and they haven't reached the peak jump height and their head hasn't collided with a tile above them
        if self.rect.y > self.initial_position_y - 96 and self.peak_jump_height_reached == False and self.head_and_tile_collided == False:
            
            # Jump and decrease the player's jump velocity 
            self.rect.y -=  self.handle_tile_collisions(movement_direction = ("y", "up"), movement_speed = 8 - self.jump_deceleration)

            # Increase the jump deceleration, so that the player moves slower as they reach the peak jump height
            self.jump_deceleration += 0.2

            # If the player has reached x tiles above where they started the jump
            if self.rect.y < self.initial_position_y - 96:
                # Set the peak height of the jump as reached
                self.peak_jump_height_reached = True

        # If the player has reached the peak height of the jump
        if self.peak_jump_height_reached == True:
            # Handle gravity
            self.handle_gravity()

    def handle_player_movement(self):

        # The distance the player travels in the x axis with each key press
        self.move_distance_x = int(300 * self.delta_time)

        # Player key-presses:

        # If the "a" key is pressed and moving left won't place the player off the screen
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left - self.move_distance_x > 0:

            # Move the player left
            self.rect.x -= self.handle_tile_collisions(movement_direction = ("x", "left"), movement_speed = self.move_distance_x)


        # If the "a" key is pressed and the player isn't at the end of the tile map
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.right + self.move_distance_x < self.last_tile_position[0]:

            # Move the player right
            self.rect.x += self.handle_tile_collisions(movement_direction = ("x", "right"), movement_speed = self.move_distance_x)


        # If the "w" key is pressed
        if pygame.key.get_pressed()[pygame.K_w] and self.allowed_to_jump == True:
            
            # Record the initial y position of the player
            self.initial_position_y = self.rect.y

            # Don't allow the player to jump
            self.allowed_to_jump = False

        # If the player is in the air and the player has pressed the input to jump
        if self.allowed_to_jump == False:
            # Start the jump algorithm
            self.jump()


        # # If the player is in the air and the player hasn't pressed the input to jump, it means that the player is floating/ walked off a "platform"
        # elif self.in_air == True and self.commence_jump == False:
        #     self.handle_gravity()
    
    def handle_tile_collisions(self, movement_direction, movement_speed = 0):
        # Calculates the distance that the player should move right before they collide with a tile, so that the player never phases through the tile

        # For each world tile that is near the player
        for tile_number, tile in self.neighbouring_tiles_dict.items():
            
            # Create a new tile rect, which is a rectangle which holds the rectangle positions of the tile as it is being seen on screen
            camera_tile_rect = pygame.Rect(tile.rect.x - self.camera_position[0], tile.rect.y - self.camera_position[1], 32, 32)

            # If the player is trying to move along the x axis
            if movement_direction[0] == "x":

                # Left side of the player colliding with the right side of the tile
                if camera_tile_rect.colliderect(self.actual_player_position[0] - movement_speed, self.actual_player_position[1], self.image.get_width(), self.image.get_height()):
                    
                    # Testing highlight
                    pygame.draw.rect(self.surface, "yellow", camera_tile_rect, 0)
                    
                    # If the player is trying to move left
                    if movement_direction[1] == "left":
                        # Move the player as much to the left as much as we can before they collide with the tiled
                        return movement_speed - (camera_tile_rect.right - (self.actual_player_position[0] - movement_speed))

                    # If the player is trying to move right
                    if movement_direction[1] == "right":

                        # If the tile to the right of the player is in the neighbouring tiles dictionary
                        if tile_number + 1 in self.neighbouring_tiles_dict.keys():
                            
                            # Create a new rect for that adjacent tile
                            adjacent_tile_rect_to_player = pygame.Rect(self.neighbouring_tiles_dict[tile_number + 1].rect.x - self.camera_position[0], self.neighbouring_tiles_dict[tile_number + 1].rect.y - self.camera_position[1], 32, 32)

                            # If there is a collision between the player and the tile to the right of the player
                            if adjacent_tile_rect_to_player.colliderect((self.actual_player_position[0] + movement_speed ), self.actual_player_position[1], self.image.get_width(), self.image.get_height()):
                                # Return 0, i.e. don't let the player move
                                return 0

                            # Note: If there is no collision, then movement speed is returned (at the end of the method)

                # Right side of the player colliding with the left side of the tile
                if camera_tile_rect.colliderect(self.actual_player_position[0] + movement_speed, self.actual_player_position[1], self.image.get_width(), self.image.get_height()):       
                    pygame.draw.rect(self.surface, "yellow", camera_tile_rect, 0)
                    
                    # If the player is trying to move left
                    if movement_direction[1] == "left":
                        
                        # If the tile to the left of the player is in the neighbouring tiles dictionary
                        if (tile_number - 1) in self.neighbouring_tiles_dict.keys():
                            
                            # Create a new rect for that adjacent tile
                            adjacent_tile_rect_to_player = pygame.Rect(self.neighbouring_tiles_dict[tile_number - 1].rect.x - self.camera_position[0], self.neighbouring_tiles_dict[tile_number - 1].rect.y - self.camera_position[1], 32, 32)

                            # If there is a collision between the player and the tile to the left of the player
                            if adjacent_tile_rect_to_player.colliderect((self.actual_player_position[0] - movement_speed ), self.actual_player_position[1], self.image.get_width(), self.image.get_height()):
                                # Return 0, i.e. don't let the player move
                                return 0

                            # Note: If there is no collision, then movement speed is returned (at the end of the method)

                    # If the player is trying to move right
                    if movement_direction[1] == "right":
                        # Move the player to the right as much as we can before they collide with the tile
                        return movement_speed - ((self.actual_player_position[3] + movement_speed) - camera_tile_rect.left)

            # If the player is trying to move along the y - axis
            if movement_direction[0] == "y":
                
                # If the bottom of the player is colliding with the top of the tile
                if camera_tile_rect.colliderect(self.actual_player_position[0], self.actual_player_position[1] + movement_speed, self.image.get_width(), self.image.get_height()):
                    
                    # If the player has reached the peak height of the jump and is still in the air, it means that they just landed on top of the tile from jumping (i.e. Once the player is back on the ground after jumping)
                    if self.peak_jump_height_reached == True and self.allowed_to_jump == False:

                        # Allow the player to jump again
                        self.allowed_to_jump = True

                        # Reset jump deceleration
                        self.jump_deceleration = 1

                        # In the event that the player's head collided with a block above it, reset self.head_and_tile_collided
                        self.head_and_tile_collided = False

                        # Reset gravity so that the player stops falling
                        self.gravity = 0

                        # Reset peak jump height reached
                        self.peak_jump_height_reached = False

                    pygame.draw.rect(self.surface, "blue", camera_tile_rect)
                    
                    # If the player is moving down
                    if movement_direction[1] == "down":
                        # Move the player down as much as we can before they collide with the tile
                        return movement_speed - ((self.actual_player_position[2] + movement_speed) - camera_tile_rect.top)

                # If the bottom of the player is colliding with the bottom of the tile
                elif camera_tile_rect.colliderect(self.actual_player_position[0], self.actual_player_position[1] - movement_speed, self.image.get_width(), self.image.get_height()):
                    
                    # Set the head and tile collided attribute to True, set the peak jump height as reached so that gravity starts taking effect.
                    # Note: This is so that gravity will pull the player down, and when the player reaches the ground again, they will be able to jump again
                    self.head_and_tile_collided = True
                    self.peak_jump_height_reached = True

                    pygame.draw.rect(self.surface, "blue", camera_tile_rect)

                    # If the player is trying to move up
                    if movement_direction[1] == "up":
                        # Move the player up as much as we can before they collide with the tile
                        return movement_speed - (camera_tile_rect.bottom - (self.actual_player_position[1] - movement_speed))

        # If it still hasn't exited the method by now, then the player must not be colliding with anything
        return movement_speed

            
    def run(self):
        
        # Find / Update the actual player position for accurate collisions
        self.find_actual_player_position()

        pygame.draw.line(self.surface, "white", (self.surface.get_width() / 2, 0), (self.surface.get_width() / 2, self.surface.get_height()))

        # Testing rect

        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()


        
        # # Create / update a mask for pixel - perfect collisions (Uncomment later when adding collisions with objects other than tiles)
        # self.mask = pygame.mask.from_surface(self.image)
