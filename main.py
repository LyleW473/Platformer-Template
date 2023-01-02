import pygame
from settings import *
from game_states_controller import GameStatesController


class Main:
    def __init__(self):

        # Pygame set-up
        pygame.init()

        # Set the caption
        pygame.display.set_caption("Maniacal")

        # Set the screen to be full screen
        self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)

        # Create an object to track time
        self.clock = pygame.time.Clock()
        
        # Create a game states controller
        self.game_states_controller = GameStatesController()

    def run(self):

        while True:
            
            # Run the game states controller
            # Note: This is where we can change game states, e.g. from the menu to ingame
            self.game_states_controller.run()
            
            # -------------------------------------
            # Update display
            pygame.display.update() 
            
            # Limit FPS to 60
            self.clock.tick(60)

if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()