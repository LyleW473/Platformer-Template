from settings import *
import pygame, sys

class Button():
    # ID used to track which menu the button will be in
    button_id = 1

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # Button ID
        self.id = Button.button_id
        # Increment the button id for the next buttons instantiated
        Button.button_id += 1  

        # Border animations
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

    def update(self, pos):
        mouse_over_button = False
        # Check for a collision between the button and the current mouse position
        if self.rect.collidepoint(pos):
            mouse_over_button = True

        # Draw the button
        self.screen.blit(self.image, self.rect)

        # Return the clicked variable to the menu
        return mouse_over_button


class Menu():
    def __init__(self):
        # Basic set-up
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # Buttons
        self.buttons_list = [] # Holds all the buttons inside a list
        self.clicked = False # Used to track whenever the buttons on the menus are clicked

        # Note: Measurements of all buttons are: (400 x 125) pixels
        # Main menu
        self.play_button = Button((screen_width / 2) - 200 , 200 , pygame.image.load("graphics/Buttons/play_button.png"))
        self.controls_button = Button((screen_width / 2) - 200, 400, pygame.image.load("graphics/Buttons/controls_button.png"))
        self.quit_button = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/quit_button.png"))

        # Controls menu
        self.back_button = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/back_button.png"))

        # Paused menu
        self.continue_button = Button((screen_width / 2) - 200, 200, pygame.image.load("graphics/Buttons/continue_button.png"))
        self.controls_button_2 = Button((screen_width / 2) - 200, 400, pygame.image.load("graphics/Buttons/controls_button.png"))
        self.quit_button_2 = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/quit_button.png"))
        
        # Add the buttons to the buttons list
        self.buttons_list.append(self.play_button)
        self.buttons_list.append(self.controls_button)
        self.buttons_list.append(self.quit_button)
        self.buttons_list.append(self.back_button)
        self.buttons_list.append(self.continue_button)
        self.buttons_list.append(self.controls_button_2)
        self.buttons_list.append(self.quit_button_2)
        # ------------------------------------------------------------------------------------------------------------------------------------------------

        # Game states
        self.in_game = False # Determines whether we are in game or not
        self.show_main_menu = True # Determines whether we show the main menu or not
        self.show_controls_menu = False # Determines whether we show the controls menu or not
        self.show_paused_menu = False # Determines whether we show the paused menu or not
        
        # Store the last menu visited so that we can go back to previous menus when the "Back" button is clicked
        self.last_menu_visited = 0 # 1 = Main menu, 2 = Paused menu

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # Animated background variables
        self.arc_height = 300
        self.arc_width = 800
        self.arc_x = 200
        self.arc_y = (screen_height / 2) - (self.arc_height / 2)
        self.arc_starting_angle = 0.5
        self.arc_finishing_angle = 3.14

        # Dictionaries for the white/red arcs
        self.white_arc_dictionary = {i:[self.arc_x, self.arc_y, self.arc_width - (i * 40), self.arc_height - (i * 15), self.arc_starting_angle + (0.314 * (i * 2)), self.arc_finishing_angle, 1] for i in range(0, 4 + 1)}
        self.red_arc_dictionary = {i:[self.arc_x, self.arc_y, self.arc_width - (i * 40), self.arc_height - (i * 15), self.arc_finishing_angle, self.arc_starting_angle - (0.314 * (i * 2)), 1] for i in range(0, 4 + 1)}
        self.arc_movement_direction = 1 # 1 = Moving right, -1 = Moving left

         # ------------------------------------------------------------------------------------------------------------------------------------------------

    def update(self, pos):
        
        # Show the background animation
        self.animate_background()

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # MAIN MENU

        if self.show_main_menu == True:

            # PLAY BUTTON
            # If the mouse is over the play button and is the mouse button is clicked
            if self.play_button.update(pos) == True and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False
                # Set the main menu to stop showing and start the game
                self.show_main_menu = False
                self.in_game = True

            # CONTROLS BUTTON
            if self.controls_button.update(pos) == True and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Display the show controls menu
                self.show_controls_menu = True
                self.show_main_menu = False

                # Set the last menu visited from the controls menu to be the paused menu
                self.last_menu_visited = 1

            # QUIT BUTTON
            # If the mouse is over the quit button and is the mouse button is clicked
            if self.quit_button.update(pos) == True and self.clicked == True:
                # Quit the game
                pygame.quit()
                sys.exit()

            # If none of the buttons above are True, that means the player clicked on empty space
            elif self.play_button.update(pos) == False and self.quit_button.update(pos) == False and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

            
        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # CONTROLS MENU

        if self.show_controls_menu == True:

            # BACK BUTTON
            if self.back_button.update(pos) == True and self.clicked == True:
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Go back to the last menu 
                if self.last_menu_visited == 1: # MAIN MENU
                    self.show_main_menu = True

                elif self.last_menu_visited == 2: # PAUSED MENU
                    self.show_paused_menu = True

                # Don't show the controls menu
                self.show_controls_menu = False

            # If none of the buttons above are True, that means the player clicked on empty space
            elif self.back_button.update(pos) == False and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # PAUSED MENU

        if self.show_paused_menu == True:
            
            # CONTINUE BUTTON
            if self.continue_button.update(pos) == True and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Go back to the main game
                self.in_game = True
                self.show_paused_menu = False

            # CONTROLS BUTTON
            if self.controls_button_2.update(pos) == True and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Display the show controls menu
                self.show_controls_menu = True
                self.show_paused_menu = False   
                
                # Set the last menu visited from the controls menu to be the paused menu
                self.last_menu_visited = 2

            # QUIT BUTTON
            # If the mouse is over the quit button and is the mouse button is clicked
            if self.quit_button_2.update(pos) == True and self.clicked == True:
                # Quit the game
                pygame.quit()
                sys.exit()

            # If none of the buttons above are True, that means the player clicked on empty space
            elif self.continue_button.update(pos) == False and self.controls_button_2.update(pos) == False and self.quit_button_2.update(pos) == False:
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False             

    def animate_background(self):

        # Fill the screen with black
        self.screen.fill("black")

        for red_arc, arc_info in self.red_arc_dictionary.items():
            # Draw red arcs onto the screen
            pygame.draw.arc(self.screen, "red", (arc_info[0], arc_info[1], arc_info[2], arc_info[3]), arc_info[4], arc_info[5])

            # If the starting angle is not equal to the finishing angle
            if arc_info[4] != arc_info[5]:
                # Increment the starting and finishing angle
                arc_info[4] += 0.0314
                arc_info[5] += 0.0314

            # Moving the arc across the screen
            arc_info[0] += 1 * self.arc_movement_direction

            # If the arc has reached the far right or far left of the screen
            if arc_info[0] == screen_width + 200 or arc_info[0] == 0 - arc_info[2] - 200:
                # Turn around and move towards the other side of the screen
                self.arc_movement_direction *= -1


        for white_arc, arc_info in self.white_arc_dictionary.items():
            # Draw red arcs onto the screen
            pygame.draw.arc(self.screen, "white", (arc_info[0], arc_info[1], arc_info[2], arc_info[3]), arc_info[4], arc_info[5])

            # Spinning the arcs
            # If the starting angle is not equal to the finishing angle
            if arc_info[4] != arc_info[5]:
                # Increment the starting and finishing angle
                arc_info[4] += 0.02
                arc_info[5] += 0.02

            # Moving the arc across the screen
            arc_info[0] += 1 * self.arc_movement_direction

            # If the arc has reached the far right or far left of the screen
            if arc_info[0] == screen_width + 200 or arc_info[0] == 0 - arc_info[2] - 200:
                # Turn around and move towards the other side of the screen
                self.arc_movement_direction *= -1


    def run(self):

        # While we aren't in-game
        while self.in_game == False:

            # Event handler
            for event in pygame.event.get():

                # If the mouse button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the self.clicked variable to True
                    self.clicked = True

                # If the exit button was pressed
                if event.type == pygame.QUIT:
                    # Close the program
                    pygame.quit()
                    sys.exit()


            # Find the position of the mouse
            self.pos = pygame.mouse.get_pos()

            # Constantly update the menu, checking for whenever the player is clicking buttons
            self.update(self.pos)

            # Play the button border animations in their respective menus
            for button in self.buttons_list:    

                # If we are in the main menu
                if self.show_main_menu:
                    # If the button is the 1st, 2nd or 3rd button instantiated
                    if button.id in {1, 2, 3}:
                        # Play the button's border animations
                        button.play_border_animations()

                # If we are in the controls menu
                elif self.show_controls_menu:
                    # If the button is the 4th button instantiated
                    if button.id in {4}:
                        # Play the button's border animations
                        button.play_border_animations()
                
                # If we are in the paused menu
                elif self.show_paused_menu:
                    # If the button is the 5th 6th or 7th button instantiated
                    if button.id in {5, 6, 7}: 
                        # Play the button's border animations
                        button.play_border_animations()
            

            # --------------------------------------
            # Update display
            pygame.display.update() 

            # Limit FPS to 60
            self.clock.tick(60)



