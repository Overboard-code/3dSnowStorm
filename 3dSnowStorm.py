#!/usr/bin/python3
"""
 3D Snow Storm Animation
 Andy Richter June 2019
"""
from __future__ import division, absolute_import, print_function, unicode_literals
import os,argparse,sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # suppress the 'Hello' from Pygame message 
import pygame
from functools import partial
from random import randrange, uniform
from math import sin, pi
X, Y, Z, D, A = 0, 1, 2, 3, 4 
FPS = 30
class SimStorm:     
    def __init__(self, num_flakes, wind, max_depth, wide, high):
        self.new_screen(wide,high)
        self.clock = pygame.time.Clock()
        self.num_flakes = num_flakes
        self.max_depth = max_depth
        self.wind = wind    # wind can be a positive or negative int.  It will cause the flakes to drift right(+) or left(-). 
        self.flakes = []    # All of the snow flake co-ordinates go here
        self.init_flakes()  # Fill the array with new random flakes  
    
    def clamp(self, n, smallest, largest): return max(smallest, min(n, largest))
    
    def init_flakes(self):  
        """ Create the Storm
            Make all of the X,Y,Z, Drift and Angle random so we can
            create new flakes all over the screen
        """
        for i in range(self.num_flakes):
            # The flakes are represented as a list of positions: [X,Y,Z] + D for D*sin(A) drift
            self.flakes.append([randrange(self.width), randrange(self.height), randrange(1, self.max_depth),
            uniform(-.5,2.2), uniform(pi, pi * 2)])
    
    def new_screen(self,width,height):
        ''' New_Screen
            Creates a new window of width and hieght or 
            recreates the window with new width and height 
        '''
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF)
        pygame.display.set_caption("Snow Storm Animator     <ESC> to quit")
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
    
    def move_and_draw_flakes(self):
        """ Move and draw the flakes """
        for flake in self.flakes:
            # Draw each flake, if it is visible on the screen, or reset it.
            # We calculate the size and speed such that distant flakes are smaller, slower and
            # darker than closer flakes. This is done using Linear Interpolation.
            LinIntvalue = float((1 - float(flake[Z]) / self.max_depth)) # This flakes Linear Interpolation.
            flake[Z] += uniform(-0.1,0.1)
            flake[Z] = max(min(flake[Z], self.max_depth), 1)
            if (0 <= flake[X] <= self.width) and (0 <= flake[Y] <= self.height) and (0 <= flake[Z] <= (self.max_depth+1)): # If on screen then draw the flake
                #flake[X] += randrange(-1, 2) + self.wind  # Let the flakes drift a little in the wind 
                drift = flake[D]*sin(flake[A]) + self.wind
                flake[X] += int(LinIntvalue * drift)  # Let the flakes drift a little in the wind
                speed = int(LinIntvalue * (self.max_depth/(2)))     # add to Y to drop the flake down
                flake[A] +=  LinIntvalue * uniform(-0.01,0.1)        # change the angle at random for the Drift 
                flake[Y] += self.clamp(speed, 2, int(self.max_depth/2))
                shade = LinIntvalue * 255
                size = int(LinIntvalue * 6.5)
                pygame.draw.circle(self.screen, (shade,shade,shade), (flake[X],flake[Y]), size)  # Draw each flake
            else:  # This flake is out of bounds. Lets make a new flake off to the side or top.
                if flake[Y] < self.height:  # Not at the bottom yet, we must've blown off one of the sides
                    if flake[X] <= 0: 
                        flake[X] = self.width # start a new flake at the right side
                    else: 
                        flake[X] = 0  # start a new flake at the left side
                else:  # We are off the bottom, start a random new flake at the top
                    flake[X] = randrange(self.width)
                    flake[Y] = 0
                flake[Z] = randrange(1, self.max_depth) # As new flakes appear, make the flake's depth random
            
    def run(self):
        """ Main Loop """
        while 1:
            for event in pygame.event.get(): # Handle Events, Just hit <ESC> to quit.
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return    
                elif event.type == pygame.VIDEORESIZE: # Reset the screen to the new size
                    self.new_screen(event.w,event.h)
            self.screen.fill((0,0,0)) # clear out the display
            self.move_and_draw_flakes() # re-draw the snow in it's current positions
            pygame.display.flip() # Animate
            self.clock.tick(FPS) # Set the frame rate Frames per Second.


#  main Loop 
if __name__ == "__main__":    
    """ range_type
        This function checks to see if a value is in a range.
        If not, raise an argparse error with a message.
    """
    def range_type(test_value, min=1, max=10):
        value = int(test_value)
        if min <= value <= max:
            return value
        else:
            raise argparse.ArgumentTypeError('value %s not in range %s to %s'%(test_value,min,max))

    pgmName =  os.path.basename(sys.argv[0])
    descStr = """ {0} simulates a fall of snow using the pygame module.  
 When run with no arguments, this program shows the default storm.
      {0} --wind 2 --flakes 600 --depth 11
      
 eg.  {0} --wind -2 -f 500
      {0} -d 9 -w 4 --flakes 755
         """.format(pgmName)
    parser = argparse.ArgumentParser(description=descStr,formatter_class=argparse.RawDescriptionHelpFormatter ) 
    # add expected arguments 
    parser.add_argument('-f','--flakes', nargs=1, dest='num_flakes', metavar="[1 to 800]", default=[600],   
                type=partial(range_type, min=1, max=800), required=False,  help="How many snow flakes in the storm. Default is %(default)s") 
    parser.add_argument('-d','--depth', nargs=1, dest='max_depth', metavar="[2 to 12]", default=[11],
                type=partial(range_type, min=2, max=12), required=False, help="How deep is the 3d effect.  Default is %(default)s")       
    parser.add_argument('-w','--wind',nargs=1, dest='wind', metavar="[-8 to 8]", default=[2], 
                type=partial(range_type, min=-8, max=8), required=False, help="Wind strength. Default is %(default)s")                 

    args = parser.parse_args(sys.argv[1:]) 
    if args.wind:
        wind =  args.wind[0]    
    if args.num_flakes:
        num_flakes =  args.num_flakes[0]
    if args.max_depth:
        max_depth =  args.max_depth[0]
    #        (num_flakes, wind, max_depth, wide, high )
    SimStorm(num_flakes, wind, max_depth, 1024, 768).run()
