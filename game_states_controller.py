import pygame, sys
from settings import *
from menu import Menu
from game import Game

class GameStatesController():
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()
        self.full_screen = True

        # Game states
        self.menu = Menu()
        self.game = Game() # The actual level

    def event_loop(self):

        # Event handler
        for event in pygame.event.get():

            # Identify the type of event
            match event.type:
                
                # Exit button on the window clicked
                case pygame.QUIT:

                    # If the exit button was pressed
                    if event.type == pygame.QUIT:
                        # Close the program
                        pygame.quit()
                        sys.exit()

                # Key presses
                case pygame.KEYDOWN:
                    
                    # Find which key was pressed
                    match event.key:
                        
                        # "f" key
                        case pygame.K_f:
                            
                            # Changing from full screen to windowed mode
                            if self.full_screen == True:
                                
                                # Change to windowed mode
                                self.screen = pygame.display.set_mode((screen_width, screen_height - 50), pygame.RESIZABLE) # -50 so the title bar is visible when exiting full screen
                                self.full_screen = False

                            # Changing from windowed to full screen mode
                            elif self.full_screen == False:
                                
                                # Change to full screen mode
                                self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
                                self.full_screen = True

                        # "Esc" key
                        case pygame.K_ESCAPE:

                            # -----------------
                            # In-game
                
                            if self.game.running == True:
                                # Show the paused menu
                                self.game.running = False
                                self.menu.show_paused_menu = True
            
    def run(self):
        
        # Run the event loop
        self.event_loop()

        # If none of the menus are being shown
        if self.menu.show_main_menu == False and self.menu.show_controls_menu == False and self.menu.show_paused_menu == False:
            
            # Run the game
            self.game.running = True
            self.game.run()

        # Otherwise    
        else:
            # Run the menus
            self.menu.run()


