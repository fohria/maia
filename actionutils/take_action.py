import logging
import aid
from chop import chop_chop

def take_action(action, stride, angle, mc):
    """ performs the selected 'action'. returns 1 only if a flower was chopped/picked
        'stride' is duration of keypress and thus how big a step is
        'angle' is how much to the left or right we will rotate camera
        'mc' is the minecraft connection object """

    if action == 'forward':
        aid.sendKey('w', stride) # move forward
        return 0
    elif action == 'backward':
        aid.sendKey('s', stride) # move backwards
        return 0
    elif action == 'left':
        aid.sendKey('a', stride) # move left
        return 0
    elif action == 'right':
        aid.sendKey('d', stride) # move right
        return 0
    elif action == 'look_left':
        aid.mouseMove('horizontally', -angle) # look left
        return 0
    elif action == 'look_right':
        aid.mouseMove('horizontally', angle) # look right
        return 0
        #return 10 # we shall now reward for looking right
    elif action == 'chop':
        flowerPicked = chop_chop(mc) # performs a chop and returns true if flower was chopped
        #logging.debug("flowerPicked returned from chop_chop is: %s" % (flowerPicked))
        return 10 if flowerPicked else 0
        #return 0
    else:
        logging.error("undefined action")
