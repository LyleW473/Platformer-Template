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
        # Attributes that determine whether the player is facing left or right
        self.facing_right = True

        # ---------------------------------------
        # Horizontal movement

        # Set the initial horizontal velocity to be 0
        self.horizontal_suvat_u = 0

        # Calculate the velocity that the player moves at given a distance that the player travels within a given time span

        # After re-arranging s = ut + 1/2(a)(t^2), v is given by the equation: (2s - a(t)^2) / 2t, where a is 0 because acceleration is constant
        time_to_travel_distance_at_final_horizontal_velocity = 0.5 # t
        distance_travelled_at_final_horizontal_velocity = 96 # s
        # Full version: self.horizontal_suvat_v = ((2 * distance_travelled_at_final_horizontal_velocity) - (0 * (time_to_travel_distance_at_final_horizontal_velocity ** 2)) / (2 * time_to_travel_distance_at_final_horizontal_velocity))
        # Simplified version:
        self.horizontal_suvat_v = ((2 * distance_travelled_at_final_horizontal_velocity) / (2 * time_to_travel_distance_at_final_horizontal_velocity))

        # Calculate the acceleration needed for the player to reach self.horizontal_suvat_v within a given time span

        # After re-arranging v = u + at, a is given by the equation: (v - u) / t, where u is 0
        time_to_reach_final_horizontal_velocity = 0.12
        # Full version: self.horizontal_suvat_a = (self.horizontal_suvat_v - 0) / time_to_reach_final_horizontal_velocity
        # Simplified version:
        self.horizontal_suvat_a = self.horizontal_suvat_v / time_to_reach_final_horizontal_velocity

        # Deceleration
        self.decelerating = False
        # Calculate the deceleration required for the player to decelerate from the final horizontal velocity to 0 (Store as absolute value)

        # After re-arranging v = u + at, a is given by the equation: (v - u) / t, where v is 0
        time_taken_to_decelerate_from_final_horizontal_velocity = 0.08
        # Full version: self.deceleration_from_final_horizontal_velocity = abs((0 - self.horizontal_suvat_v) / time_taken_to_decelerate_from_final_horizontal_velocity)
        # Simplified version:
        self.deceleration_from_final_horizontal_velocity = self.horizontal_suvat_v / time_taken_to_decelerate_from_final_horizontal_velocity

        # ---------------------------------------
        # Jumping 
        
        self.allowed_to_jump = True
        self.allowed_to_double_jump = False

        # The desired height of the initial jump and double jump
        self.desired_jump_height = TILE_SIZE * 2 # 64
        self.desired_double_jump_height = (TILE_SIZE * 2) + (TILE_SIZE / 2) # 80

        # The desired time for the player to reach that jump height from the ground (in seconds)
        self.desired_time_to_reach_jump_height = 0.28
        self.desired_time_to_reach_double_jump_height = 0.3

        # The constant acceleration is given by the equation: - ( (2s) / (t^2) ), where s is the desired height and t is the desired time to reach the jump height
        self.jumping_suvat_a = - ((2 * self.desired_jump_height) / (self.desired_time_to_reach_jump_height ** 2))
        # The initial velocity is given by the equation: 2s / t, where s is the desired height and t is the desired time to reach the jump height
        self.jumping_suvat_u = (2 * self.desired_jump_height) / self.desired_time_to_reach_jump_height

        # ---------------------------------------
        # Dynamic jumping
        self.jump_power = 0
        self.performing_power_jump = False

        # The desired time for the player to reach the power jump height from the ground (The height variable is declared as a local variable inside the handle movement method)
        self.desired_time_to_reach_power_jump_height = 0.32

        # The chosen jump power indicator version that the player selected in the settings (YET TO IMP<EMENT)
        self.chosen_jump_power_indicator_version = "Special-Middle"

        # Dictionary possibly for players to change between jump power indicator versions inside the menus
        # Values are: jump_power_indicator_y, jump_power_indicator_height, Draw rect y position, Draw rect height
        # The dictionary for the different versions of the jump power indicators
        self.jump_power_indicator_versions_dict = {
            "Top": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3 * TILE_SIZE)),
            min(round(self.jump_power), 3 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3 * TILE_SIZE)) - TILE_SIZE,
            TILE_SIZE + min(round(self.jump_power), 3 * TILE_SIZE)
            ],

            "Middle": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)),
            min(round(self.jump_power), 3.5 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)) - (0.5 * TILE_SIZE),
            TILE_SIZE + min(round(self.jump_power), 3.5 * TILE_SIZE)

            ],

            "Bottom": [
            max(self.rect.bottom - (self.desired_jump_height + round(self.jump_power)), self.rect.bottom - (5 * TILE_SIZE)),
            min(self.desired_jump_height + round(self.jump_power), 5 * TILE_SIZE),
            max(self.rect.bottom - (self.desired_jump_height + round(self.jump_power)), self.rect.bottom - (5 * TILE_SIZE)), 
            min(self.desired_jump_height + round(self.jump_power), 5 * TILE_SIZE),
            ],
            "Special-Middle": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)), 
            min(round(self.jump_power), 3.5 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)) - (0.5 * TILE_SIZE),
            TILE_SIZE + min(round(self.jump_power), 3.5 * TILE_SIZE),
            (self.rect.top + (0.5 * TILE_SIZE)) - (4.5 * TILE_SIZE), 
            4.5 * TILE_SIZE 
            ]
            }
            
        # ---------------------------------------
        # Falling
        self.falling = False

        # The desired height of the fall
        self.desired_fall_height = 80
        # The desired time for the player to reach that fall height from the ground (in seconds)
        self.desired_time_to_reach_fall_height = 0.35

        # The constant acceleration is given by the equation: - ( (2s) / (t^2) ), where s is the desired height and t is the desired time to reach the jump height 
        self.falling_suvat_a = - ((2 * self.desired_fall_height) / (self.desired_time_to_reach_fall_height ** 2))
        # The initial velocity is set to 0, which is when the player is where the player momentarily has 0 velocity and will start to fall.
        self.falling_suvat_u = 0 

        # ---------------------------------------------------------------------------------
        # Collisions
        """
        self.camera_position = None # Position of the camera. This is updated inside "Game" class
        self.last_tile_position = None # Position of the last tile that the player can be on. This will be updated by "Game" when the level is created
        self.closest_ground_tile = None # Used to hold the closest ground tile to the player.
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

    def reset_movement_attributes(self):

        # Once the player is back on the ground, the following attributes need to be reset
        # If the player is 0 tiles away from the ground, then they must be on the ground
        if self.closest_ground_tile != None and self.rect.colliderect(pygame.Rect(self.closest_ground_tile.rect.x, self.closest_ground_tile.rect.y - 1, self.closest_ground_tile.rect.width, self.closest_ground_tile.rect.height)):

            # Allow the player to jump
            self.allowed_to_jump = True

            # Don't allow the player to jump
            self.allowed_to_double_jump = False

            # The initial speed of the jump should be set back to default
            self.jumping_suvat_u = (2 * self.desired_jump_height) / self.desired_time_to_reach_jump_height

            # Acceleration needs to be reset (In case that the player also double jumped)
            self.jumping_suvat_a = - ((2 * self.desired_jump_height) / (self.desired_time_to_reach_jump_height ** 2))

            # Set falling to False
            self.falling = False

            # Set the falling speed back to 0
            self.falling_suvat_u = 0

    def jump(self):

        # The method used to move the player when jumping or double jumping 

        # Equation used: s = vt + 1/2(a)(t^2)
        self.jumping_suvat_s = (self.jumping_suvat_u * self.delta_time) + (0.5 * self.jumping_suvat_a * (self.delta_time ** 2))
        
        # Move the player up / down based on the displacement
        new_position = self.rect.y 

        # If the the displacement is positive, it means we are at the stage in the parabola where we are moving up
        if self.jumping_suvat_s > 0:
            # Set the new position, based on if there are any collisions or not
            new_position -= self.handle_tile_collisions(movement_direction = ("y", "up"), movement_speed = self.jumping_suvat_s)

        # If the displacement is zero or negative, it means we are at the stage in the parabola where we are moving down
        elif self.jumping_suvat_s <= 0:
            # Set the new position, based on if there are any collisions or not
            new_position -= self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.jumping_suvat_s)

        
        """ Set the player's position based on whether "new position + self.rect.height" (which is the bottom of the player rect) is greater than the closest ground tile.
        - The int is so that if the position of the bottom of the player was 320.72829995... and the top of the tile was 320, the position should be truncated.
        - The round is so that if the position of the bottom of the player was 319.92381232... and the top of the tile was 320, the position should be rounded up.
        """
        
        # If we are at the stage in the jump where the player is moving up
        if self.jumping_suvat_s > 0:
            # Set the player's y position as the rounded new position
            self.rect.y = round(new_position)

        # If we are at the stage in the jump where the player is moving down
        elif self.jumping_suvat_s <= 0:
            
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
        self.jumping_suvat_u += (self.jumping_suvat_a * self.delta_time)

    def check_and_perform_power_jump(self):

        # The method used to check if the player can power jump, and if they are entering the correct input, perform the power jump

        # If the player is on the ground
        if self.allowed_to_jump == True and self.allowed_to_double_jump == False:
            
            # If the player is holding the spacebar button
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                
                # Set the attribute that the player is performing a power jump to True
                self.performing_power_jump = True

                # Draw and update the jump power indicator
                self.draw_jump_power_indicator()

                # If the current height generated is less than the maximum height the player can jump (5.5 x 32 pixels high)
                if (self.desired_jump_height + self.jump_power <= (5.5  * TILE_SIZE)):
                    # Keep increasing the jump power
                    self.jump_power += 112 * self.delta_time # Add 112 every second

            # If the player has released the spacebar button
            if (pygame.key.get_pressed()[pygame.K_SPACE] == False and self.jump_power > 0):

                # Set the desired power jump height

                # If the power jump height is greater than or equal to 5.5 tiles (tile size of 32)
                if self.desired_jump_height + round(self.jump_power) < (5.5 * TILE_SIZE):
                    # Set the power jump to a rounded number of the normal jump height with the jump power added on top
                    desired_power_jump_height = self.desired_jump_height + round(self.jump_power)

                # If the power jump height is greater than or equal to 5.5 tiles (tile size of 32)
                elif self.desired_jump_height + round(self.jump_power) >= (5.5 * TILE_SIZE):
                    # Set the power jump height to be at maximum, 5.5 tiles high
                    desired_power_jump_height = (5.5 * TILE_SIZE)

                # Set the new acceleration with a new height 
                self.jumping_suvat_a = - ((2 * (desired_power_jump_height))) / (self.desired_time_to_reach_power_jump_height ** 2)

                # Set the new initial speed with a new height
                self.jumping_suvat_u = (2 * (desired_power_jump_height)) / self.desired_time_to_reach_power_jump_height

                # Don't allow the player to jump (initial jump)
                self.allowed_to_jump = False
                
                # Allow the player to double jump
                self.allowed_to_double_jump = True

                # Reset the jump power
                self.jump_power = 0

                # Reset the player's horizontal velocity 
                self.horizontal_suvat_u = 0

                # Reset the attribute that the player is performing a power jump back to False
                self.performing_power_jump = False

                # Make the player jump
                self.jump()

    def draw_jump_power_indicator(self):
        """
        - The jump power indicator will only show a height that is (5 * TILE_SIZE) tall, but the amount that the player actually jumps is 5.5 tiles high.
            - This is so that the player has some room for error when trying to reach areas higher than 5 tiles from their current position
        


        # The maximum height of the jump power indicator will be (5 * TILE_SIZE)
        # 4 Versions: 

        # ---------------------------------------
        - One that draws from the top of the player's rect

        # The maximum height of the jump power indicator will be (5 * TILE_SIZE)
        # Note: The "+ 1" is because the player's desired jump height is 64, and thats starting from the bottom of the player.
        jump_power_indicator_y = max(self.rect.top - round(self.jump_power), self.rect.top - (3 * TILE_SIZE))
        jump_power_indicator_height = min(round(self.jump_power), 3 * TILE_SIZE)

        # Draw the jump power indicator
        pygame.draw.rect(self.surface, "white", (self.rect.left - 20 , jump_power_indicator_y - TILE_SIZE, 10, TILE_SIZE + jump_power_indicator_height), 0)
        pygame.draw.rect(self.surface, "black", (self.rect.left - 20 , jump_power_indicator_y - TILE_SIZE, 10, TILE_SIZE + jump_power_indicator_height), 2)

        # ---------------------------------------
        - One that draws from midpoint of the player's rect

        # The maximum height of the jump power indicator will be (5 * TILE_SIZE)
        jump_power_indicator_y = max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE))
        jump_power_indicator_height = min(round(self.jump_power), 3.5 * TILE_SIZE)

        # Draw the jump power indicator
        pygame.draw.rect(self.surface, "white", (self.rect.left - 20 , jump_power_indicator_y - (0.5 * TILE_SIZE), 10, TILE_SIZE + jump_power_indicator_height), 0)
        pygame.draw.rect(self.surface, "black", (self.rect.left - 20 , jump_power_indicator_y - (0.5 * TILE_SIZE), 10, TILE_SIZE + jump_power_indicator_height), 2)
        
        # ---------------------------------------
        - One that draws from the bottom of the player:

        # The maximum height of the jump power indicator will be (5 * TILE_SIZE)
        jump_power_indicator_y = max(self.rect.bottom - (self.desired_jump_height + round(self.jump_power)), self.rect.bottom - (5 * TILE_SIZE))
        jump_power_indicator_height = min(self.desired_jump_height + round(self.jump_power), 5 * TILE_SIZE)

        # Draw the jump power indicator
        pygame.draw.rect(self.surface, "white", (self.rect.left - 20 , jump_power_indicator_y, 10, jump_power_indicator_height), 0)
        pygame.draw.rect(self.surface, "black", (self.rect.left - 20 , jump_power_indicator_y, 10, jump_power_indicator_height), 2)

        # ---------------------------------------
        - One that draws from the bottom of the player but has a static indicator bar already spawned

        # The maximum height of the jump power indicator will be (5 * TILE_SIZE)
        jump_power_indicator_y = max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE))
        jump_power_indicator_height = min(round(self.jump_power), 3.5 * TILE_SIZE)

        # Draw the jump power indicator
        pygame.draw.rect(self.surface, "black", ((self.rect.left - 20), (self.rect.top + (0.5 * TILE_SIZE)) - (4.5 * TILE_SIZE), 10, 4.5 * TILE_SIZE), 0)
        pygame.draw.rect(self.surface, "white", (self.rect.left - 20 , jump_power_indicator_y - (0.5 * TILE_SIZE), 10, TILE_SIZE + jump_power_indicator_height), 0)
        pygame.draw.rect(self.surface, "black", (self.rect.left - 20 , jump_power_indicator_y - (0.5 * TILE_SIZE), 10, TILE_SIZE + jump_power_indicator_height), 2)

        """ 

        # Update the jump power indicator versions dictionary (This is because the self.jump_power will be different with each draw)
        self.jump_power_indicator_versions_dict = {
            "Top": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3 * TILE_SIZE)),
            min(round(self.jump_power), 3 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3 * TILE_SIZE)) - TILE_SIZE,
            TILE_SIZE + min(round(self.jump_power), 3 * TILE_SIZE)
            ],

            "Middle": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)),
            min(round(self.jump_power), 3.5 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)) - (0.5 * TILE_SIZE),
            TILE_SIZE + min(round(self.jump_power), 3.5 * TILE_SIZE)

            ],

            "Bottom": [
            max(self.rect.bottom - (self.desired_jump_height + round(self.jump_power)), self.rect.bottom - (5 * TILE_SIZE)),
            min(self.desired_jump_height + round(self.jump_power), 5 * TILE_SIZE),
            max(self.rect.bottom - (self.desired_jump_height + round(self.jump_power)), self.rect.bottom - (5 * TILE_SIZE)), 
            min(self.desired_jump_height + round(self.jump_power), 5 * TILE_SIZE),
            ],
            "Special-Middle": [
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)), 
            min(round(self.jump_power), 3.5 * TILE_SIZE),
            max(self.rect.top - round(self.jump_power), self.rect.top - (3.5 * TILE_SIZE)) - (0.5 * TILE_SIZE),
            TILE_SIZE + min(round(self.jump_power), 3.5 * TILE_SIZE),
            (self.rect.top + (0.5 * TILE_SIZE)) - (4.5 * TILE_SIZE), 
            4.5 * TILE_SIZE 
            ]
            }
        
        # Draw the jump power indicator

        # Set the width
        jump_power_indicator_width = 10

        # If the player is facing right
        if self.facing_right == True:
            # Draw the jump power indicator on the right side of the player
            jump_power_indicator_x = self.rect.right + jump_power_indicator_width

        # If the player is facing left
        else:
            # Draw the jump power indicator on the left side of the player
            jump_power_indicator_x = self.rect.left - (2 * jump_power_indicator_width)
        
        # The static bar only for the "Special-Middle" version
        if self.chosen_jump_power_indicator_version == "Special-Middle":
            pygame.draw.rect(self.surface, "black", (jump_power_indicator_x, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][4], jump_power_indicator_width, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][5]), 0)

        # The jump power indicator for all versions
        pygame.draw.rect(self.surface, "white", (jump_power_indicator_x, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][2], jump_power_indicator_width, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][3]), 0)
        pygame.draw.rect(self.surface, "black", (jump_power_indicator_x, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][2], jump_power_indicator_width, self.jump_power_indicator_versions_dict[self.chosen_jump_power_indicator_version][3]), 2)

    def fall(self):

        # The method used to move the player when falling

        # Equation used: s = vt + 1/2(a)(t^2)
        self.falling_suvat_s = (self.falling_suvat_u * self.delta_time) + (0.5 * self.falling_suvat_a * (self.delta_time ** 2))

        # Move the player up / down based on the displacement
        new_position = self.rect.y 

        # Set the new position, based on if there are any collisions or not
        new_position -= self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.falling_suvat_s)
        
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
        self.falling_suvat_u += (self.falling_suvat_a * self.delta_time)
    
    def handle_horizontal_movement(self):

        # Hold the current x position of the player in temporary variables 
        position_x, position_x_2 = self.rect.x, self.rect.x

        # If the "a" key is pressed
        if pygame.key.get_pressed()[pygame.K_a]:
            
            # If the player isn't decelerating currently
            if self.decelerating == False:

                # Set the player to face left (allows players to change where the jump power indicator is drawn on the screen)
                self.facing_right = False

                # If the player is not performing a power jump currently
                if self.performing_power_jump == False:

                    # ---------------------------------------------------------------------------------
                    # Acceleration

                    # If the current velocity has not reached the final velocity set for the player
                    if self.horizontal_suvat_u < self.horizontal_suvat_v:
                        # Increase the current velocity
                        self.horizontal_suvat_u += (self.horizontal_suvat_a * self.delta_time)

                    # Limit the current velocity to the final velocity set for the player (in case that the current velocity is greater)
                    self.horizontal_suvat_u = min(self.horizontal_suvat_u, self.horizontal_suvat_v)

                    # Set the distance travelled based on the current velocity
                    self.horizontal_suvat_s = ((self.horizontal_suvat_u * self.delta_time) + (0.5 * self.horizontal_suvat_a * (self.delta_time ** 2)))

                    # ---------------------------------------------------------------------------------
                    # Moving the player

                    # If moving left will place the player out of the screen
                    if self.rect.left - self.horizontal_suvat_s <= 0:
                        # Set the player's x position to be at 0
                        self.rect.left = 0

                    # Otherwise
                    elif self.rect.left - self.horizontal_suvat_s > 0:
                        # Move the player left
                        position_x += self.handle_tile_collisions(movement_direction = ("x", "left"), movement_speed = - self.horizontal_suvat_s)
                        self.rect.x = round(position_x)


        # If the "d" key is pressed
        if pygame.key.get_pressed()[pygame.K_d]:

            # If the player isn't decelerating currently
            if self.decelerating == False:
                
                # Set the player to face right (allows players to change where the jump power indicator is drawn on the screen)
                self.facing_right = True

                # If the player is not performing a power jump currently
                if self.performing_power_jump == False:
                    
                    # ---------------------------------------------------------------------------------
                    # Acceleration

                    # If the current velocity has not reached the final velocity set for the player
                    if self.horizontal_suvat_u < self.horizontal_suvat_v:
                        # Increase the current velocity
                        self.horizontal_suvat_u += (self.horizontal_suvat_a * self.delta_time)

                    # Limit the current velocity to the final velocity set for the player (in case that the current velocity is greater)
                    self.horizontal_suvat_u = min(self.horizontal_suvat_u, self.horizontal_suvat_v)

                    # Set the distance travelled based on the current velocity
                    self.horizontal_suvat_s = ((self.horizontal_suvat_u * self.delta_time) + (0.5 * self.horizontal_suvat_a * (self.delta_time ** 2)))

                    # ---------------------------------------------------------------------------------
                    # Moving the player

                    # If moving right will place the player out of the tile map / out of the screen
                    if self.rect.right + self.horizontal_suvat_s >= self.last_tile_position[0]:
                        # Set the player's right position to be at the last tile position in the tile map
                        self.rect.right = self.last_tile_position[0]

                    # Otherwise
                    else:
                        # Move the player right
                        position_x_2 += self.handle_tile_collisions(movement_direction = ("x", "right"), movement_speed = self.horizontal_suvat_s)
                        self.rect.x = round(position_x_2)

        # ---------------------------------------------------------------------------------
        # Deceleration

        # If the player has let go of both horizontal movement input keys or if the deceleration has already started, but the player tried to stop it by going against the direction of deceleration
        if (pygame.key.get_pressed()[pygame.K_a] == False and pygame.key.get_pressed()[pygame.K_d] == False) or self.decelerating == True:
            
            # If the player is not charging a power jump
            if self.jump_power == 0:
                
                # Set the decelerating player attribute to True
                self.decelerating = True

                # If the player has stopped decelerating
                if self.horizontal_suvat_u == 0:
                    # Set the decelerating player attribute back to False
                    self.decelerating = False

                # If the player's current velocity is greater than 0
                if self.horizontal_suvat_u > 0:
                    # Decelerate the player / decrease the velocity
                    self.horizontal_suvat_u -= (self.deceleration_from_final_horizontal_velocity * self.delta_time)

                # Limit the current velocity to 0
                self.horizontal_suvat_u = max(self.horizontal_suvat_u, 0)

                # Set the distance travelled based on the current velocity
                self.horizontal_suvat_s = ((self.horizontal_suvat_u * self.delta_time) + (0.5 * self.horizontal_suvat_a * (self.delta_time ** 2)))

                # If the player was facing right 
                if self.facing_right == True:

                    # If moving right will place the player out of the tile map / out of the screen
                    if self.rect.right + self.horizontal_suvat_s >= self.last_tile_position[0]:
                        # Set the player's right position to be at the last tile position in the tile map
                        self.rect.right = self.last_tile_position[0]

                    # Otherwise
                    else:
                        # Move the player right
                        position_x_2 += self.handle_tile_collisions(movement_direction = ("x", "right"), movement_speed = self.horizontal_suvat_s)
                        self.rect.x = round(position_x_2)

                # If the player was facing left
                elif self.facing_right == False:
        
                    # If moving left will place the player out of the screen
                    if self.rect.left - self.horizontal_suvat_s <= 0:
                        # Set the player's x position to be at 0
                        self.rect.left = 0

                    # Otherwise
                    elif self.rect.left - self.horizontal_suvat_s > 0:
                        # Move the player left
                        position_x += self.handle_tile_collisions(movement_direction = ("x", "left"), movement_speed = - self.horizontal_suvat_s)
                        self.rect.x = round(position_x)

    def handle_player_movement(self):
        
        # ---------------------------------------------------------------------------------
        # Horizontal movement

        # Handle horizontal movement
        self.handle_horizontal_movement()
        
        # ---------------------------------------------------------------------------------
        # Vertical movement
        
        # ---------------------------------------
        # Jumping
        # Note: Normal jumping is within the gamestates controller (This is so the player doesn't hold down the "w" key, which will cause the player to keep jumping)
        pygame.draw.line(self.surface, "white", (0, self.rect.bottom - ( 5 * TILE_SIZE)), (self.surface.get_width(), self.rect.bottom - ( 5 * TILE_SIZE)), 1)
        pygame.draw.line(self.surface, "white", (0, self.rect.bottom - ( 5.5 * TILE_SIZE)), (self.surface.get_width(), self.rect.bottom - ( 5.5 * TILE_SIZE)), 1)

        # ---------------------------------------
        # Dynamic / Power jumping

        # Check for input to power jump, and performs the power jump if the conditions are met
        self.check_and_perform_power_jump()

        """ 
        The following check is used so that when the player presses the input to jump, it will keep moving the player up until they reach the ground again. This is because when the player is on the ground,
        self.allowed_to_jump is constantly set to True, so the player will never actually jump. The jump method is called once in the event handler in the game states controller to get the player off the ground
        initially, and then the following code will keep repeating that until the jump is complete.
        """
        # If the player is in the air and the player has pressed the input to jump
        if self.allowed_to_jump == False:
            # Start the jump algorithm 
            self.jump()

        # ---------------------------------------
        # Falling

        # If there is no closest ground tile or the player is not colliding with the closest ground tile
        if self.closest_ground_tile == None or self.rect.colliderect(pygame.Rect(self.closest_ground_tile.rect.x, self.closest_ground_tile.rect.y - 1, self.closest_ground_tile.rect.width, self.closest_ground_tile.rect.height)) == False:

            """
            1st check: Player hasn't been set to falling and the player has not jumped yet
            """
            # If the player hasn't been set to falling already and the player is on the ground
            if (self.falling == False) and (self.allowed_to_jump == True and self.allowed_to_double_jump == False):
                self.falling = True

            # If the player has jumped or double jumped whilst falling
            elif ((self.falling == True) and (self.allowed_to_jump == False and self.allowed_to_double_jump == True)) or ((self.falling == True) and (self.allowed_to_jump == False and self.allowed_to_double_jump == False)):
                # Stop falling 
                self.falling = False
                self.falling_suvat_u = 0

        # If the player has been set to falling
        if self.falling == True:
            # Start the falling algorithm
            self.fall()

    def control_gravity_strength(self):
        # SAVE FOR LATER FOR SOMETHING ELSE 
        # Controls the strength of gravity and checks for collisions with the ground when falling down.
        # Also resets the jump related attributes when the player is on the ground

        # # Increase the player's y position by the amount it is allowed to move by (Player moving down)
        # position_y = self.rect.y
        # position_y += self.handle_tile_collisions(movement_direction = ("y", "down"), movement_speed = self.gravity)
        # self.rect.y = round(position_y)

        # #print(self.initial_y_position, self.rect.bottom)
        
        # # ---------------------------------------------------------------------------------
        # # Calculating the distance between the closest ground tile and the player

        # # If there is no closest ground tile, the player is floating 
        # if self.closest_ground_tile == None:
        #     # Temporary value, adjust this later on when deciding on gravity limits depending on height
        #     num_of_tiles_away_from_closest_ground_tile = 5

        # # If there is a closest ground tile
        # if self.closest_ground_tile != None:
        #     # Calculate the number of tiles away the player is from the ground
        #     num_of_tiles_away_from_closest_ground_tile = abs(self.rect.bottom - (self.rect.bottom % TILE_SIZE)- self.closest_ground_tile.rect.top) / (TILE_SIZE)
        pass

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
        print(self.horizontal_suvat_u)
        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()

        # Reset the movement attributes if the conditions are met
        self.reset_movement_attributes()

        # # Create / update a mask for pixel - perfect collisions (Uncomment later when adding collisions with objects other than tiles)
        # self.mask = pygame.mask.from_surface(self.image)
