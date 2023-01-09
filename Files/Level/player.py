import pygame, time
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

        self.handle_input = False

        # Jumping 
        self.allowed_to_jump = True
        self.allowed_to_double_jump = False

        # The desired height of the jump
        self.desired_jump_height = 96
        # The desired time for the player to reach that jump height from the ground
        self.desired_time_to_reach_jump_height = 0.35

        # The constant acceleration is given by the equation: - ( (2s) / (t^2) ), where s is the desired height and t is the desired time to reach the jump height
        self.suvat_a = - ((2 * self.desired_jump_height) / (self.desired_time_to_reach_jump_height ** 2))
        # The initial velocity is given by the equation: 2s / t, where s is the desired height and t is the desired time to reach the jump height
        self.suvat_u = (2 * self.desired_jump_height) / self.desired_time_to_reach_jump_height

        # ---------------------------------------------------------------------------------
        # Collisions
        """
        self.actual_player_position = None : Actual position of the player when the camera position is subtracted from the player rect's position
        self.camera_position = None # Position of the camera. This is updated inside "Game"d
        self.last_tile_position = None # Position of the last tile that the player can be on. This will be updated by "Game" when the level is created
        self.closest_ground_tile = None # Used to hold the closest ground tile to the player, which will help to determine the strength of gravity
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
        #self.draw(surface = self.surface, x = (self.rect.x - self.camera_position[0]), y = (self.rect.y - self.camera_position[1]))

    # ---------------------------------------------------------------------------------
    # Movement           

    def reset_jump_attributes(self):

        # Once the player is back on the ground, the following attributes need to be reset
        
        # If the player is 0 tiles away from the ground, then they must be on the ground
        if self.closest_ground_tile != None and self.rect.colliderect(pygame.Rect(self.closest_ground_tile.rect.x, self.closest_ground_tile.rect.y - 1, self.closest_ground_tile.rect.width, self.closest_ground_tile.rect.height)):

            # Allow the player to jump
            self.allowed_to_jump = True

            # Don't allow the player to jump
            self.allowed_to_double_jump = False

            # The initial speed of the jump should be set back to default
            self.suvat_u = (2 * self.desired_jump_height) / self.desired_time_to_reach_jump_height

    def jump(self):

        # Equation used: s = vt + 1/2(a)(t^2)
        self.suvat_s = (self.suvat_u * self.delta_time) + (0.5 * self.suvat_a * (self.delta_time ** 2))
        
        # Move the player up / down based on the displacement
        new_position = self.rect.y 

        # If the the displacement is positive, it means we are at the stage in the parabola where we are moving up
        if self.suvat_s > 0:
            # Set the new position, based on if there are any collisions or not
            new_position -= self.handle_tile_collisions(movement_direction = ("y", "up"), movement_speed = abs(self.suvat_s))

        # If the displacement is zero or negative, it means we are at the stage in the parabola where we are moving down
        elif self.suvat_s <= 0:
            print(abs(self.suvat_s))
            # Set the new position, based on if there are any collisions or not
            new_position += self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = abs(self.suvat_s))
        
        # Set the player's position to the rounded new position (Rounded for accuracy)
        self.rect.y = round(new_position)

        # Set the new value for v based on the delta time  
        self.suvat_u += (self.suvat_a * self.delta_time)

    def handle_player_movement(self):
        
        # ---------------------------------------------------------------------------------
        # Horizontal movement

        # The distance the player travels in the x axis with each key press

        pygame.draw.line(self.surface, "white", (self.last_tile_position[0], 0), (self.last_tile_position[0], self.surface.get_height()))

        # Hold the current x position of the player in temporary variables 
        position_x, position_x_2 = self.rect.x, self.rect.x

        # Acceleration and initial speed are testing values, so may change
        suvat_a = 2
        suvat_u = 192
        # s = ut + 1/2(a)(t)^2
        suvat_s = (suvat_u * self.delta_time) + (0.5 * suvat_a * (self.delta_time ** 2))

        # If the "a" key is pressed and moving left won't place the player off the screen
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left > 0:
            # Move the player left
            position_x -= self.handle_tile_collisions(movement_direction = ("x", "left"), movement_speed = suvat_s)
            self.rect.x = round(position_x)

        # If the "d" key is pressed and the player isn't at the end of the tile map
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.right < self.last_tile_position[0]:
            # Move the player right
            position_x_2 += self.handle_tile_collisions(movement_direction = ("x", "right"), movement_speed = suvat_s)
            self.rect.x = round(position_x_2)

        # ---------------------------------------------------------------------------------
        # Vertical movement
        """ 
        The following check is used so that when the player presses the input to jump, it will keep moving the player up until they reach the ground again. This is because when the player is on the ground,
        self.allowed_to_jump is constantly set to True, so the player will never actually jump. The jump method is called once in the event handler in the game states controller to get the player off the ground
        initially, and then the following code will keep repeating that until the jump is complete.
        """
        # If the player is in the air and the player has pressed the input to jump
        if self.allowed_to_jump == False:
            # Start the jump algorithm 
            self.jump()
    
    def control_gravity_strength(self):
        # SAVE FOR LATER FOR SOMETHING ELSE 
        # Controls the strength of gravity and checks for collisions with the ground when falling down.
        # Also resets the jump related attributes when the player is on the ground

        # Increase the player's y position by the amount it is allowed to move by (Player moving down)
        position_y = self.rect.y
        position_y += self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.gravity)
        self.rect.y = round(position_y)

        #print(self.initial_y_position, self.rect.bottom)
        
        # ---------------------------------------------------------------------------------
        # Calculating the distance between the closest ground tile and the player

        # If there is no closest ground tile, the player is floating 
        if self.closest_ground_tile == None:
            # Temporary value, adjust this later on when deciding on gravity limits depending on height
            num_of_tiles_away_from_closest_ground_tile = 5

        # If there is a closest ground tile
        if self.closest_ground_tile != None:
            # Calculate the number of tiles away the player is from the ground
            num_of_tiles_away_from_closest_ground_tile = abs(self.rect.bottom - (self.rect.bottom % TILE_SIZE)- self.closest_ground_tile.rect.top) / (TILE_SIZE)

    # ---------------------------------------------------------------------------------
    # Collisions      

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
                          
    def handle_tile_collisions(self, movement_direction, movement_speed):
        # Calculates the distance that the player should move right before they collide with a tile, so that the player never phases through the tile

        # For each world tile that is near the player
        for tile_number, tile in self.neighbouring_tiles_dict.items():
            
            # Create a new tile rect, which is a rectangle which holds the rectangle positions of the tile as it is being seen on screen
            camera_tile_rect = pygame.Rect(tile.rect.x - self.camera_position[0], tile.rect.y - self.camera_position[1], TILE_SIZE, TILE_SIZE)

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
                            adjacent_tile_rect_to_player = pygame.Rect(self.neighbouring_tiles_dict[tile_number + 1].rect.x - self.camera_position[0], self.neighbouring_tiles_dict[tile_number + 1].rect.y - self.camera_position[1], TILE_SIZE, TILE_SIZE)

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
                            adjacent_tile_rect_to_player = pygame.Rect(self.neighbouring_tiles_dict[tile_number - 1].rect.x - self.camera_position[0], self.neighbouring_tiles_dict[tile_number - 1].rect.y - self.camera_position[1], TILE_SIZE, TILE_SIZE)

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

                    # # If the player is moving down
                    if movement_direction[1] == "down":
                        print(self.rect.bottom, self.rect.bottom + (movement_speed - ((self.actual_player_position[2] + movement_speed) - camera_tile_rect.top)), camera_tile_rect.top)
                        # Move the player down as much as we can before they collide with the tile
                        return movement_speed - ((self.actual_player_position[2] + movement_speed) - camera_tile_rect.top)

                # If the bottom of the player is colliding with the bottom of the tile
                elif camera_tile_rect.colliderect(self.actual_player_position[0], self.actual_player_position[1] - movement_speed, self.image.get_width(), self.image.get_height()):

                    # If the player is trying to move up
                    if movement_direction[1] == "up":
                        # Move the player up as much as we can before they collide with the tile
                        return movement_speed - (camera_tile_rect.bottom - (self.actual_player_position[1] - movement_speed))

        #print(movement_direction, movement_speed)
        # If it still hasn't exited the method by now, then the player must not be colliding with anything
        return movement_speed

    def run(self):
        
        # Find / Update the actual player position for accurate collisions
        self.find_actual_player_position()

        pygame.draw.line(self.surface, "white", (self.surface.get_width() / 2, 0), (self.surface.get_width() / 2, self.surface.get_height()))

        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()

        # Reset the jumping attributes if the conditions are met
        self.reset_jump_attributes()

        # # Create / update a mask for pixel - perfect collisions (Uncomment later when adding collisions with objects other than tiles)
        # self.mask = pygame.mask.from_surface(self.image)
