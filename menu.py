from settings import *
import pygame, sys

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = pygame.display.set_mode((screen_width, screen_height))

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
        self.clicked = False # Used to track whenever the buttons on the menus are clicked

        # Note: Measurements of all buttons are: (400 x 125) pixels
        # Main menu
        self.play_button = Button((screen_width / 2) - 200 , 200 , pygame.image.load("graphics/Buttons/play_button.png"))
        self.controls_button = Button((screen_width / 2) - 200, 400, pygame.image.load("graphics/Buttons/controls_button.png"))
        self.quit_button = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/quit_button.png"))

        # Controls menu
        self.back_button = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/back_button.png"))
        self.return_to_main_menu_button = Button((screen_width / 2) - 200, 400, pygame.image.load("graphics/Buttons/return_to_main_menu_button.png"))


        # Paused menu
        self.continue_button = Button((screen_width / 2) - 200, 200, pygame.image.load("graphics/Buttons/continue_button.png"))
        self.controls_button_2 = Button((screen_width / 2) - 200, 400, pygame.image.load("graphics/Buttons/controls_button.png"))
        self.quit_button_2 = Button((screen_width / 2) - 200, 600, pygame.image.load("graphics/Buttons/quit_button.png"))

        # ------------------------------------------------------------------------------------------------------------------------------------------------

        # Game states
        self.in_game = False # Determines whether we are in game or not
        self.show_main_menu = True # Determines whether we show the main menu or not
        self.show_controls_menu = False # Determines whether we show the controls menu or not
        self.show_paused_menu = False # Determines whether we show the paused menu or not
        
        # Store the last menu visited so that we can go back to previous menus when the "Back" button is clicked
        self.last_menu_visited = 0 # 1 = Main menu, 2 = Paused menu

    def update(self, pos):
        # MAIN MENU

        if self.show_main_menu == True:
            self.screen.fill("white")

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
            self.screen.fill("green")

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
            self.screen.fill("red")
            
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

            # --------------------------------------
            # Update display
            pygame.display.update() 

            # Limit FPS to 60
            self.clock.tick(60)



