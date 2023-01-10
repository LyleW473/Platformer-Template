import pygame, time
from Global.settings import *
from game_states_controller import GameStatesController


class Main:
    def __init__(self):

        # Pygame set-upw
        pygame.init()

        # Set the caption
        pygame.display.set_caption("Maniacal")

        # Set the screen to be full screen 
        self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN, depth = 32)
        
        # Create a game states controller
        self.game_states_controller = GameStatesController()

        # Time
        # Record the previous frame that was played
        self.previous_frame = time.perf_counter()
        
        # Create an object to track time
        self.clock = pygame.time.Clock()
        self.chosen_framerate = 30
        
    def run(self):
 
        while True:
            
            # Limit FPS to 60
            self.clock.tick(self.chosen_framerate)

            # Calculate delta time 
            delta_time = time.perf_counter() - self.previous_frame
            self.previous_frame = time.perf_counter()

            # Run the game states controller
            # Note: This is where we can change game states, e.g. from the menu to ingame
            self.game_states_controller.run(delta_time)
            
            # -------------------------------------
            # Update display
            pygame.display.update() 
            

if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()