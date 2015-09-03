import logging
import numpy as np
from PIL import ImageGrab
import gamewindow
from qlearner import observe_state
import time
from qlearner import get_indices
import dill

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

def is_it_red(frame, config):
    """ returns true if there are any pixels from flower_colors in frame
        since red values are in principle unique for the flowers in our pasture,
        this works well"""

    flower_colors_outer = [[205.0/255,6.0/255,9.0/255],
                    [182.0/255,5.0/255,11.0/255],
                    [242.0/255,7.0/255,15.0/255],
                    [142.0/255,2.0/255,5.0/255]]
    flower_colors_inner = [[71.0/255,1.0/255,2.0/255],
                    [140.0/255,3.0/255,5.0/255],
                    [57.0/255,1.0/255,2.0/255],
                    [96.2/255,2.0/255,4.0/255]]

    pixel_array = np.take(frame,config['pixel_indices'])

    count = 0  # want to find at least these many red pixels
    for pixel in pixel_array:
        for color in flower_colors_outer:
            if all(pixel == color):
                count += 1
        for color in flower_colors_inner:
            if all(pixel == color):
                count += 1
    return count

size = 50
config = {}
config['pixel_indices'] = get_indices(size)

gw = gamewindow.GameWindow(size)

counter = 1

states = []

while counter != 0:

    logging.debug("taking screenshot in 3 seconds...")
    time.sleep(1)
    logging.debug("2...")
    time.sleep(0)
    logging.debug("1...")
    time.sleep(0)
    state = observe_state(gw)

#    logging.debug("checking for red now")
#    if is_it_red(state,config):
#        logging.debug("RED!")
#    logging.debug("checked for red")

#    logging.debug("checking for red now")
#    red_count = is_it_red(state,config)
#    logging.debug("finished red check")#

#    logging.debug("red pixels in frame: %s" % (red_count))

    time.sleep(0)

    counter -= 1

#print state.shape
#print state.reshape()

pixel_array = np.take(state,config['pixel_indices'])
logging.debug("pixelarray")

print "pixelarray reshaped"
reshaped = pixel_array.reshape(size,size,3)

upleft, botleft, upright, botright = reshaped[:size//2, :size//2], reshaped[size//2:, :size//2], reshaped[:size//2, size//2:], reshaped[size//2:, size//2:]

flower_colors_outer = [[205.0/255,6.0/255,9.0/255],
                [182.0/255,5.0/255,11.0/255],
                [242.0/255,7.0/255,15.0/255],
                [142.0/255,2.0/255,5.0/255]]
flower_colors_inner = [[71.0/255,1.0/255,2.0/255],
                [140.0/255,3.0/255,5.0/255],
                [57.0/255,1.0/255,2.0/255],
                [96.2/255,2.0/255,4.0/255]]

logging.debug("starting counters")
count_ul = 0  # want to find at least these many red pixels
for row in upleft:
    for pixel in row:
        for color in flower_colors_outer:
            if all(pixel == color):
                count_ul += 1
        for color in flower_colors_inner:
            if all(pixel == color):
                count_ul += 1

count_ur = 0
for row in upright:
    for pixel in row:
        for color in flower_colors_outer:
            if all(pixel == color):
                count_ur += 1
        for color in flower_colors_inner:
            if all(pixel == color):
                count_ur += 1

count_bl = 0
for row in botleft:
    for pixel in row:
        for color in flower_colors_outer:
            if all(pixel == color):
                count_bl += 1
        for color in flower_colors_inner:
            if all(pixel == color):
                count_bl += 1

count_br = 0
for row in botright:
    for pixel in row:
        for color in flower_colors_outer:
            if all(pixel == color):
                count_br += 1
        for color in flower_colors_inner:
            if all(pixel == color):
                count_br += 1

logging.debug("counting over")
logging.debug("%s reds in upper left" % (count_ul))
logging.debug("%s reds in upper right" % (count_ur))
logging.debug("%s reds in bottom left" % (count_bl))
logging.debug("%s reds in bottom right" % (count_br))

logging.debug("count says %s to chopping" % (count_ul*count_ur*count_bl*count_br > 0))

def is_quadrant_red(quadrant):
     indices = xrange(0,len(quadrant),3)
     red_quadrant = np.take(quadrant, indices)
     red_sum = np.sum(red_quadrant)
     red_avg = np.sum(red_quadrant) / len(red_quadrant)

     logging.debug("red avg: %s" % (red_avg))

     indices = xrange(1,len(quadrant),3)
     green_quadrant = np.take(quadrant, indices)
     green_sum = np.sum(green_quadrant)
     green_avg = np.sum(green_quadrant) / len(green_quadrant)

     logging.debug("green avg: %s" % (green_avg))

     indices = xrange(2,len(quadrant),3)
     blue_quadrant = np.take(quadrant, indices)
     blue_sum = np.sum(blue_quadrant)
     blue_avg = np.sum(blue_quadrant) / len(blue_quadrant)

     logging.debug("blue avg: %s" % (blue_avg))

     is_red = red_avg / (0.5 * (green_avg + blue_avg))
     logging.debug("redcalc: %s" % (is_red))

     if is_red > 2:
         return 1
     else:
         return 0

logging.debug("doing avg sum check for red now")
logging.debug("upleft")
upleft_red = is_quadrant_red(np.ravel(upleft))
logging.debug("upright")
upright_red = is_quadrant_red(np.ravel(upright))
logging.debug("botleft")
botleft_red = is_quadrant_red(np.ravel(botleft))
logging.debug("botright")
botright_red = is_quadrant_red(np.ravel(botright))
logging.debug("avg says %s to chopping" % (upleft_red*upright_red*botleft_red*botright_red > 0))
logging.debug("avg red check done")

#logging.debug(upleft)
#logging.debug("bla")
#logging.debug(np.ravel(upleft))













#logging.debug(np.any( [flower_colors in pixel_array] ))



















#logging.debug("will check now")
#def red_check(state, rgb_state, flower_colors):
#    pixel_array = np.take(state,rgb_state)
#    count = 5
#    for value in pixel_array:
#        if value in np.nditer(flower_colors):
#            count -= 1
#            if count == 0:
#                return True
#    return False
#print red_check(state,rgb_state,flower_colors)
#logging.debug("check done")#

#print "cutoff"
#print red_vals





























#flower_colors = [(205,6,9)]

#logging.debug("printing frame now...")
#logging.debug(frame)

#logging.debug("checking with numpy")
#logging.debug(np.in1d(frame, flower_colors))
#for pixel in np.nditer(frame):
#    if np.in1d(np.any(flower_colors),pixel):
#        print "FOUND ONE!"
#logging.debug("done")
#logging.debug("checking with python")
#logging.debug(any(flower_colors) in frame)
#if any(px in frame for px in flower_colors):
#    print "FOUND ONE!"
#logging.debug("done")
#logging.debug("checking explicityly")




#frame = gw.grab_frame()
#flat_frame = np.ravel(frame)

#logging.debug("printing flattened frame now..")
#logging.debug(flat_frame)

#normed_frame = np.multiply(1.0/255, flat_frame)

#logging.debug("printing normed frame now")
#logging.debug(normed_frame)

#indices = xrange(0,len(flat_frame),3)
#red_frame = np.take(flat_frame, indices)

#logging.debug("printing REDs from flattened frame")
#logging.debug(red_frame)

#red_sum = np.sum(red_frame)
#logging.debug(red_sum / len(red_frame))

#red_normed_frame = np.take(normed_frame, indices)

#red_normed_sum = np.sum(red_normed_frame)
#logging.debug(red_normed_sum / len(red_normed_frame))

# R G B R G B R G B
# 0 1 2 3 4 5 6 7 8

# 0 + 3 + 3

# >>> a = [4, 3, 5, 7, 6, 8]
# >>> indices = [0, 1, 4]
# >>> np.take(a, indices)
# array([4, 3, 6])

# indices = []
#red_vals = [205.0/255, 182.0/255, 242.0/255, 142.0/255]

#indices = xrange(0,len(state),3)
#[0,1,2],[3,4,5]
#print [ [x] ]
#red_state = np.take(state, indices)
