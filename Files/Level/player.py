import pygame
from Global.generic import Generic
from Global.settings import *

class Player(Generic):
    def __init__(self, x, y):

        # Position of the last tile that the player can be on. This will be updated by "Game" when the level is created
        self.last_tile_position = None

        # Button border animations
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

        # Inherit from the objects class, which has the basic attributes and methods of all objects
        super().__init__(x = x, y = y, image = self.animation_list[0])

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

    def handle_player_movement(self):

        # The distance the player with each key press
        move_distance = 200
        
        # If the "a" key is pressed and moving left won't place the player off the screen
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left - (move_distance * self.delta_time) > 0:
            # Move the player left
            self.rect.x -= move_distance * self.delta_time

        # If the "a" key is pressed and the player isn't at the end of the tile map
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.right + (move_distance * self.delta_time) < self.last_tile_position[0]:
            # Move the player right
            self.rect.x += move_distance * self.delta_time

        # If the "w" key is pressed
        if pygame.key.get_pressed()[pygame.K_w]:
            # Move the player up
            self.rect.y -= move_distance * self.delta_time

        # If the "s" key is pressed
        if pygame.key.get_pressed()[pygame.K_s]:
            # Move the player down
            self.rect.y += move_distance * self.delta_time

    def run(self):

        # Play animations
        self.play_animation()

        # Track player movement
        self.handle_player_movement()
