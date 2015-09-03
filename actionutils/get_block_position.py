import logging
from mcpi.vec3 import Vec3
import mcpi.block as block
import aid
import time

def get_block_position(mc):
    """ requires sword in player hand. right clicks to get position of block.
        if a block is in range, it returns block position otherwise returns Vec3(999,999,999)
        'mc' is minecraft connection object """

    position = Vec3(999,999,999) # hack because Vec3 doesn't support None
    #logging.debug("inside get_block_position, position is now: %s" % (position))
    aid.mouseClick('right') # needed to catch event properly, without this events are empty first
    time.sleep(0.05)

    hitcounter = 0

    while True:
        blockHits = mc.events.pollBlockHits()
        aid.mouseClick('right')
        #logging.debug("clicked right button")
        if blockHits:
            for blockHit in blockHits:
                #logging.debug("blockhit")
                #logging.debug(blockHit.pos)
                hitcounter += 1
            if hitcounter > 1:
                position = blockHits[hitcounter-1].pos
            else:
                position = blockHits[0].pos

            #logging.debug("i shall now return the position which is: %s" % (position))
            break
        else:
            #logging.debug("no block in range, returning position which is: %s" % (position))
            break

    mc.events.clearAll()
    return position
