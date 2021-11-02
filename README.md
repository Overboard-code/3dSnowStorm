# 3d Snow Storm
Uses PyGame or Python Turtle to simulate a 3d Snow Storm in a window. You can choose number of flakes, wind and depth of field on the command line. Uses Linear Interpolation to show the Flakes as; slower, smaller and darker, as they increase in depth. 
```
The pygame window is re-sizeable but it will take the snow a little while to catch up with the new size. 

usage: 3dSnowStorm.py [-h] [-f [1 to 800]] [-d [2 to 12]] [-w [-8 to 8]]

 3dSnowStorm.py Simulates a fall of snow using the pygame module.
 When run with no arguments, this program shows the default storm.
      3dSnowStorm.py --wind 2 --flakes 600 --depth 11

 eg.  3dSnowStorm.py --wind -2 -f 500
      3dSnowStorm.py -d 9 -w 4 --flakes 755


optional arguments:
  -h, --help            show this help message and exit
  -f [1 to 800], --flakes [1 to 800]
                        How many snow flakes in the storm. Default is [600]
  -d [2 to 12], --depth [2 to 12]
                        How deep is the 3d effect. Default is [11]
  -w [-8 to 8], --wind [-8 to 8]
                        Wind strength. Default is [2]
```
