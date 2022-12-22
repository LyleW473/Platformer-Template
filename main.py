import pygame, sys
from settings import *
from menu import Menu


class Main:

    def __init__(self):

        # Pygame set-up
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        # Menu
        self.menu = Menu()

    def run(self):

        while True:
            
            # Event handler
            for event in pygame.event.get():

                # If the exit button was pressed
                if event.type == pygame.QUIT:
                    # Close the program
                    pygame.quit()
                    sys.exit()
                
                # If a button (key) was pressed
                if event.type == pygame.KEYDOWN:
                    
                    # If the key was the "Esc" button
                    if event.key == pygame.K_ESCAPE:
                        # Set in-game attribute to be False and show the paused menu
                        self.menu.in_game = False
                        self.menu.show_paused_menu = True
                        

            # --------------------------------------
            # Menus

            # If we aren't in-game (i.e. in the menus)
            if self.menu.in_game == False:
                # Run the menu 
                self.menu.run()

            # Main game

            # If we are in-game 
            elif self.menu.in_game == True:

                # Fill the screen with blue
                self.screen.fill("dodgerblue4")

            # -------------------------------------
            # Update display
            pygame.display.update() 
            # Limit FPS to 60
            self.clock.tick(60)


    
if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()