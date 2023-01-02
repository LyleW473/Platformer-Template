import pygame
from settings import * 

class Button():
    def __init__(self, x, y, image):
        
        # Basic attributes
        self.screen = pygame.display.get_surface()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Border animations attributes
        self.border_animation_x = self.rect.x
        self.border_animation_y = self.rect.y
        self.border_animation_line_thickness = 10

    def play_border_animations(self):

        # Draw the "square" onto the button
        pygame.draw.line(self.screen, "red4", (self.border_animation_x, self.border_animation_y), (self.border_animation_x + self.border_animation_line_thickness, self.border_animation_y), self.border_animation_line_thickness)
    
        # Top left to top right
        # If the border animation isn't at the top right corner of the button
        if self.border_animation_x < self.rect.x + self.width - ( self.border_animation_line_thickness / 2) and self.border_animation_y == self.rect.y:
            # Move to the right
            self.border_animation_x += 1

        # Once the border animation is at the top right corner of the button and has become the same width as the line thickness
        else:

            # If the border animation is not at the bottom right (from the top right) of the button
            if self.border_animation_y < self.rect.y + self.height and self.border_animation_x >= self.rect.x + self.width - ( self.border_animation_line_thickness / 2):
                # Move down
                self.border_animation_y += 1 

            # Once the border animation is at the bottom right corner of the button
            else:
                # If the border animation is not at the bottom left corner of the button
                if self.border_animation_x > self.rect.x - (self.border_animation_line_thickness / 2):
                    # Move left
                    self.border_animation_x -= 1

                # Once the border animation is at the bottom left corner of the button
                else:
                    # If the border animation is not at the top left of the button
                    if self.border_animation_y > self.rect.y - self.border_animation_line_thickness:
                        # Move up
                        self.border_animation_y -= 1 

    def draw(self):
        self.screen.blit(self.image, (self.rect))