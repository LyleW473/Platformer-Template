import pygame, sys
from settings import *
from menu import Menu
from game import Game

class GameStatesController():
    def __init__(self):

        # Screen
        self.screen = pygame.display.get_surface()

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
                            pass

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


