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

        # The desired height of the initial jump
        self.desired_jump_height = TILE_SIZE * 2 # 64
        self.desired_double_jump_height = (TILE_SIZE * 2) + (TILE_SIZE / 2) # 80

        # The desired time for the player to reach that jump height from the ground (in seconds)
        self.desired_time_to_reach_jump_height = 0.28
        self.desired_time_to_reach_double_jump_height = 0.3

        # The constant acceleration is given by the equation: - ( (2s) / (t^2) ), where s is the desired height and t is the desired time to reach the jump height
        self.suvat_a = - ((2 * self.desired_jump_height) / (self.desired_time_to_reach_jump_height ** 2))
        # The initial velocity is given by the equation: 2s / t, where s is the desired height and t is the desired time to reach the jump height
        self.suvat_u = (2 * self.desired_jump_height) / self.desired_time_to_reach_jump_height

        # ---------------------------------------------------------------------------------
        # Collisions
        """
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

            # Acceleration needs to be reset (In case that the player also double jumped)
            self.suvat_a = - ((2 * self.desired_jump_height) / (self.desired_time_to_reach_jump_height ** 2))

    def jump(self):

        # Equation used: s = vt + 1/2(a)(t^2)
        self.suvat_s = (self.suvat_u * self.delta_time) + (0.5 * self.suvat_a * (self.delta_time ** 2))
        
        # Move the player up / down based on the displacement
        new_position = self.rect.y 

        # If the the displacement is positive, it means we are at the stage in the parabola where we are moving up
        if self.suvat_s > 0:
            # Set the new position, based on if there are any collisions or not
            new_position -= self.handle_tile_collisions(movement_direction = ("y", "up"), movement_speed = self.suvat_s)

        # If the displacement is zero or negative, it means we are at the stage in the parabola where we are moving down
        elif self.suvat_s <= 0:
            # Set the new position, based on if there are any collisions or not
            new_position -= self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.suvat_s)

        
        """ Set the player's position based on whether "new position + self.rect.height" (which is the bottom of the player rect) is greater than the closest ground tile.
        - The int is so that if the position of the bottom of the player was 320.72829995... and the top of the tile was 320, the position should be truncated.
        - The round is so that if the position of the bottom of the player was 319.92381232... and the top of the tile was 320, the position should be rounded up.
        """
        
        # If we are at the stage in the jump where the player is moving up
        if self.suvat_s > 0:
            # Set the player's y position as the rounded new position
            self.rect.y = round(new_position)

        # If we are at the stage in the jump where the player is moving down
        elif self.suvat_s <= 0:
            
            # If there is not closest ground tile
            if self.closest_ground_tile == None:
                # Set the player's position as the new position (Normal falling)
                self.rect.y = round(new_position)

            # If the bottom of the player is greater than the top of the closest ground tile
            elif (new_position + self.rect.height) > self.closest_ground_tile.rect.top:

                # At low frame rates, as a last case scenario, do another check to see if the bottom of the player would still be greater than top of the closest ground tile
                if int(new_position + self.rect.height) > self.closest_ground_tile.rect.top:
                    # If it is, set the player's bottom to be at the top of the closest ground tile
                    self.rect.bottom = self.closest_ground_tile.rect.top
                
                # Otherwise
                else:
                    # Truncate the new position, so the player won't be overlapping the closest ground tile
                    self.rect.y = int(new_position)

            # If the bottom of the player is less than or equal to the top of the tile
            elif (new_position + self.rect.height) <= self.closest_ground_tile.rect.top:
                # Set the position of the player as the rounded value (rounds up), so the player won't be overlapping the closest ground tile
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
        if pygame.key.get_pressed()[pygame.K_a]: #and self.rect.left > 0:
            
            # If moving left will place the player out of the screen
            if self.rect.left - suvat_s <= 0:
                # Set the player's x position to be at 0
                self.rect.left = 0
            # Otherwise
            elif self.rect.left - suvat_s > 0:
                # Move the player left
                position_x += self.handle_tile_collisions(movement_direction = ("x", "left"), movement_speed = - suvat_s)
                self.rect.x = round(position_x)

        # If the "d" key is pressed and the player isn't at the end of the tile map
        if pygame.key.get_pressed()[pygame.K_d]: #and self.rect.right < self.last_tile_position[0]:
            
            # If moving right will place the player out of the tile map / out of the screen
            if self.rect.right + suvat_s >= self.last_tile_position[0]:
                # Set the player's right position to be at the last tile position in the tile map
                self.rect.right = self.last_tile_position[0]
            # Otherwise
            else:
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
                          
    def handle_tile_collisions(self, movement_direction, movement_speed):
        # Calculates the distance that the player should move right before they collide with a tile, so that the player never phases through the tile

        # self.rect.y - movement_speed because going up = subtracting, going down = adding
        y_collisions = pygame.Rect(self.rect.x, self.rect.y - movement_speed, self.rect.width, self.rect.height).collidedict(self.neighbouring_tiles_dict)
        x_collisions = pygame.Rect(self.rect.x + movement_speed, self.rect.y, self.rect.width, self.rect.height).collidedict(self.neighbouring_tiles_dict)


        # If there is a y collision
        if y_collisions != None and movement_direction[0] == "y":
            pygame.draw.rect(self.surface, "green", (y_collisions[0].rect.x - self.camera_position[0], y_collisions[0].rect.y - self.camera_position[1], y_collisions[0].rect.width, y_collisions[0].rect.height))
            
            # If the player is moving down
            if movement_speed < 0:
                # Return the negative value of how much the player should move. 
                # Note: This is because self.rect.y - (- dy) is the same as self.rect.y + dy
                return - (movement_speed - ((self.rect.bottom + movement_speed) - y_collisions[0].rect.top))
            
            # If the player is moving up
            elif movement_speed > 0:
                # Move the player as much as we can before overlapping with the tile
                return movement_speed - (y_collisions[0].rect.bottom - (self.rect.y - movement_speed))

        # If there is a horizontal collision
        elif x_collisions != None and movement_direction[0] == "x":
            pygame.draw.rect(self.surface, "green", (x_collisions[0].rect.x - self.camera_position[0], x_collisions[0].rect.y - self.camera_position[1], x_collisions[0].rect.width, x_collisions[0].rect.height))
            
            # If the player is moving left
            if movement_speed < 0:
                # Move the player as much as we can before overlapping with the tile
                return movement_speed + (x_collisions[0].rect.right - (self.rect.left + movement_speed))

            # If the player is moving right
            if movement_speed > 0:
                # Move the player as much as we can before overlapping with the tile
                return movement_speed - ((self.rect.right + movement_speed) - x_collisions[0].rect.left)

        # If there are no collisions, then move the player by movement_speed
        return movement_speed

    def run(self):
        
        pygame.draw.line(self.surface, "white", (self.surface.get_width() / 2, 0), (self.surface.get_width() / 2, self.surface.get_height()))

        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()

        # Reset the jumping attributes if the conditions are met
        self.reset_jump_attributes()

        # # Create / update a mask for pixel - perfect collisions (Uncomment later when adding collisions with objects other than tiles)
        # self.mask = pygame.mask.from_surface(self.image)
