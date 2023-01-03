import pygame

class GlowingParticle:
    def __init__(self, surface, random_destination):

        # Draw the particle on the surface passed as a parameter
        self.surface = surface

        # Set the destination as the random destination passed as a parameter
        self.destination = random_destination

        # For a single particle
        self.particle_information = [ [radius, radius, pygame.Surface((radius * 2, radius * 2)), (20, 20, 20), 1] for radius in range(6, 20, 2)]


    def draw(self):

        # Particle information for each particle: [original_particle_radius, particle_radius, particle_surface, particle_colour, particle_radius_operation_direction, glowing_particle_destination]
        for i in range (0, len(self.particle_information)):
            
            # -------------------------------------------------------------------------------------
            # Change the colour of the particle

            # # If this particle is the last particle
            # if i == len(self.particle_information) - 1:
            #     # Set the particle colour to red
            #     self.particle_information[i][3] = "red"

            # -------------------------------------------------------------------------------------
            # Dynamic radius

            # If the radius of the particle it is greater than or equal to the original radius of particle information + 5
            if self.particle_information[i][1] >= self.particle_information[i][0] + 5:
                # Start decrementing the radius
                self.particle_information[i][4] = -1

            # If the radius of the particle it is less than or equal to the original radius of particle information - 5
            if self.particle_information[i][1] <= self.particle_information[i][0] - 5:
                # Start incrementing the radius
                self.particle_information[i][4] = 1

            # Increase or decrease the radius, depending on the current radius
            self.particle_information[i][1] += 20 * self.particle_information[i][4] * self.delta_time
            
            # Resize the particle's surface so that all surfaces are still centered
            self.particle_information[i][2] = pygame.Surface(((self.particle_information[i][1] * 2) + 5,( self.particle_information[i][1] * 2) + 5))

            # -------------------------------------------------------------------------------------
            # Drawing the glowing particle onto the main screen

            # Draw the circle in the center of the particle surface
            pygame.draw.circle(surface = self.particle_information[i][2], color = self.particle_information[i][3], center = (self.particle_information[i][1], self.particle_information[i][1]), radius = self.particle_information[i][1], width = 0)

            # Set the colour key of the surface to black
            self.particle_information[i][2].set_colorkey("black")

            # Draw the particle surface onto the main screen at a random destination
            self.surface.blit(source = self.particle_information[i][2], dest = (self.destination[0] - self.particle_information[i][1] , self.destination[1] - self.particle_information[i][1]), special_flags = pygame.BLEND_RGB_ADD)