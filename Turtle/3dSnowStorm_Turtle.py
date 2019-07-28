"""
 3D Snow Storm Simulation
 Andy Richter June 2019
"""
import os, sys, turtle, argparse
from functools import partial
from random import randrange
from math import sin
     
FPS = 180      # constant: refresh about xx times per second
TIMER_VALUE = 1000//FPS # the timer value in milliseconds for timer events
SPEED = 60     #  Speed throttle

class TurtleStormSim:     
    def __init__(self, num_flakes, max_depth, wide, high, wind):
        self.screen = turtle.Screen()
        self.screen.clear()
        self.screen.setup(wide,high)
        self.screen.setworldcoordinates(-0.01,high+0.01,wide+0.01,-0.01)
        self.screen.title("Snow Storm Simulation")
        self.screen.bgcolor('black')
        self.width = wide
        self.height = high
        #print ("Canvas is (" + str(self.width) + "," + str(self.height) + ")")
        self.num_flakes = num_flakes
        self.max_depth = max_depth
        self.should_draw = True
        self.flakes = []
        self.wind = wind*(FPS/2)/FPS
        self.colorlist = ["White","Snow","White Smoke","Ivory","Gainsboro","Light Grey","Light slate gray","Silver","Slate Gray","Dark Grey","Grey","Dim Grey","Dark Grey"]
        self.speedlist = [11,10,9,8,7,6,5,4,3,3,2,2]
        self.sizelist = [7,7,6,6,5,4,4,3,3,2,2,1,1]
        self.init_flakes()
        #self.master.bind('<Escape>', self.close)
        
    def init_turtle(self,colr,size):
        t = turtle.Turtle()
        t.hideturtle()
        t.getscreen().tracer(0)
        t.speed(0)
        t.pensize(int(size))
        t.color(colr)
        t.penup()
        return t
    
    def close(event):
        sys.exit() # if you want to exit the entire thing
    
    def init_flakes(self):
        """ Create the Storm """
        for i in range(self.num_flakes):
            flake = {}
            flake['t'] = self.init_turtle(self.colorlist[0],2)
            flake['X'] = randrange(0 , self.width)
            flake['Y'] = randrange(0 , self.height)
            flake['Z'] = randrange(1, self.max_depth)
            flake['drift'] = randrange(1,4)
            flake['size'] = self.sizelist[ flake['Z']-1 ]
            flake['shade'] = self.colorlist[ flake['Z']-1 ] 
            flake['speed'] = self.speedlist[ flake['Z']-1 ]*(SPEED)/(FPS)
            # The flakes are represented as a list of positions: [X,Y,Z] size and shade
            self.flakes.append(flake)

    def draw(self):
        if self.should_draw == False: # There is no change. Don't draw and return immediately
            return
        for flake in self.flakes:
            flake['t'].clear() # clear the current drawing
            flake['t'].color(flake['shade'])
            flake['t'].goto(flake['X'],flake['Y'])
            flake['t'].dot(flake['size'])
        self.should_draw = False # just finished drawing, wait until next time
        
    def move_flakes(self):
        """ Move and draw the flakes """
        wide = turtle.window_width()
        high = turtle.window_height()
        #print ("Canvas is (" + str(self.width) + "," + str(self.height) + ")")
        if self.height != high or self.width != wide:
            self.__init__(self.num_flakes,self.max_depth,wide,high,self.wind)
        for flake in self.flakes:
            # Draw each flake, if it is visible on the screen, else reset it.
            # We calculate the size and speed such that distant flakes are smaller and slower 
            # than closer flakes. Similarly, we make sure that distant flakes are
            # darker than closer flakes. This is done using Linear Interpolation.
            if (0 <= flake['X'] <= self.width) and (0 <= flake['Y'] <= self.height): # If on screen then draw the flake
                flake['X'] += flake['drift'] * sin(1) + self.wind  # Let the flakes drift a little in the wind  
                flake['Y'] += flake['speed']
            else:  # This flake is out of bounds reset it
                if flake['Y'] < self.height:  # Not at the bottom yet we must've blown off the sides
                    if flake['X'] <= 0: 
                        flake['X'] = self.width
                    else: 
                        flake['X'] = 0
                else:  # We are off the bottom reset to the top
                    flake['X'] = randrange(0,self.width)
                    flake['Y'] = 0
                flake['Z'] = randrange(1, self.max_depth) # As new flakes appear on screen make the distance random
                flake['size']  = self.sizelist[ flake['Z']-1 ]
                flake['shade'] = self.colorlist[ flake['Z']-1 ]
                flake['speed'] = self.speedlist[ flake['Z']-1 ] *(SPEED)/FPS
        self.should_draw = True        
        self.screen.ontimer(self.move_flakes,TIMER_VALUE)
            
    def run(self):
        """ Main Loop """
        self.move_flakes()
        while 1:
            self.draw()
            self.screen.update() 
                 
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
    descStr = """ {0} Simulates a fall of snow using the pygame module.  
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
#        (num_flakes, max_depth, wide, high, wind)
    TurtleStormSim(num_flakes, max_depth, 1024, 768, wind).run()
    turtle.mainloop()
