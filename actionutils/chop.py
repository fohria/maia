import logging
import time
from get_block_position import get_block_position
from mcpi.vec3 import Vec3
import mcpi.block as block
import aid

def chop_chop(mc):
    """ clicks left mouse button, chopchop!
        returns true if a flower was chopped, otherwise false.
        'mc' is minecraft connection object """

    currentBlockPosition = get_block_position(mc)
    if currentBlockPosition == Vec3(999,999,999):
        logging.debug("no block in range")
        return False
    else:
        blockPreChop = mc.getBlock(currentBlockPosition)
        #logging.debug("blockprechop is: %s" % (blockPreChop))
        aid.mouseClick('left')
        time.sleep(0.05) # allow block to change type
        blockPostChop = mc.getBlock(currentBlockPosition)
        #logging.debug("blockpostchop is: %s" % (blockPostChop))

    if blockPreChop == 38 and blockPostChop != 38:
        #logging.debug("that was a flowah! returning true good sir")
        #time.sleep(2)
        return True
    else:
        #logging.debug("that was not a flower, so get your shit together!")
        #time.sleep(2)
        return False
