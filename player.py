class Player:
    def __init__(self):
        pass

        # # TEMPORARY STORAGE:
        # # Button border animations
        # self.border_animation_list = []
        # self.border_animation_index = 0 
        # self.border_animation_cooldown = 3000 # Milliseconds
        # self.border_animation_frame_time = pygame.time.get_ticks()

        # # Animation loading
        # for i in range(0, 2): # 2 images at the moment
        #     # Load the border animation images
        #     border_animation_image = pygame.transform.scale(pygame.image.load(f"graphics/Buttons/border_animations/{i}.png"), (430, 155))
        #     # Append the animation image to the animations list
        #     self.border_animation_list.append(border_animation_image)

    # def play_border_animations(self):

        # # Draw the animation frame onto the screen
        # self.screen.blit(self.border_animation_list[self.border_animation_index], (self.rect.x - 20, self.rect.y - 20))

        # # If enough time has passed since the last frame was played or since the animation was reset
        # if (pygame.time.get_ticks() - self.border_animation_frame_time) > self.border_animation_cooldown:

        #     # If the border animation index isn't at the end of the list 
        #     if (self.border_animation_index < len(self.border_animation_list) - 1 ):
        #         # Increment the index
        #         self.border_animation_index += 1

        #     # If the border animation index is at the end of the list
        #     else:
        #         # Reset the index
        #         self.border_animation_index = 0
                    
        #     # Record the time that the frame was played / that the animation was reset
        #     self.border_animation_frame_time = pygame.time.get_ticks()


    # def run(self):
            #         # # Play the button border animations in their respective menus
            # for button in self.buttons_list:
                
            #     # If we are in the main menu
            #     if self.show_main_menu:
            #         # If the button is the 1st, 2nd or 3rd button instantiated
            #         if button.id in {1, 2, 3}:
            #             # Play the button's border animations
            #             button.play_border_animations()

            #     # If we are in the controls menu
            #     elif self.show_controls_menu:
            #         # If the button is the 4th button instantiated
            #         if button.id in {4}:
            #             # Play the button's border animations
            #             button.play_border_animations()
                
            #     # If we are in the paused menu
            #     elif self.show_paused_menu:
            #         # If the button is the 5th 6th or 7th button instantiated
            #         if button.id in {5, 6, 7}: 
            #             # Play the button's border animations
            #             button.play_border_animations()