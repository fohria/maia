import mcpi.minecraft as minecraft
import mcpi.block as block
from random import randint
from mcpi.vec3 import Vec3

def create_pasture():
    # pasturesize sets how many blocks around player to shape
    pastureSize = 20
    wallHeight = 2

    mc = minecraft.Minecraft.create()

    # x and z is the plane, y is vertical (x,y,z)
    playerPosition = mc.player.getTilePos()

    # need this if we cannot move player manually or if in water
    #playerPosition = Vec3(playerPosition.x, playerPosition.y+25, playerPosition.z)

    # blocktype 38 is red flower, 2 is grass

    # create cube of air around player
    mc.setBlocks(playerPosition.x-pastureSize, playerPosition.y, playerPosition.z-pastureSize, playerPosition.x+pastureSize, playerPosition.y+pastureSize, playerPosition.z+pastureSize, block.AIR.id)

    # create grass to walk on in area under the air
    mc.setBlocks(playerPosition.x-pastureSize, playerPosition.y-1, playerPosition.z-pastureSize, playerPosition.x+pastureSize, playerPosition.y-1, playerPosition.z+pastureSize, block.GRASS.id)

    # randomly place flowers in our pasture
    xpos = range(playerPosition.x - pastureSize, playerPosition.x + pastureSize+1)
    zpos = range(playerPosition.z - pastureSize, playerPosition.z + pastureSize+1)

    for x in xpos:
        for z in zpos:
            #flowerProbability = randint(1,4)
            flowerProbability = 1 # place flowers EVERYWHERE!
            if flowerProbability == 1:
                mc.setBlock(x, playerPosition.y, z, 38)

    # create wall around the area so player can't get out without jumping
    mc.setBlocks(playerPosition.x-pastureSize+1, playerPosition.y-1, playerPosition.z-pastureSize+1, playerPosition.x+pastureSize+1, playerPosition.y+wallHeight, playerPosition.z-pastureSize+1, block.GRASS.id)
    mc.setBlocks(playerPosition.x-pastureSize+1, playerPosition.y-1, playerPosition.z-pastureSize+1, playerPosition.x-pastureSize+1, playerPosition.y+wallHeight, playerPosition.z+pastureSize+1, block.GRASS.id)
    mc.setBlocks(playerPosition.x-pastureSize+1, playerPosition.y-1, playerPosition.z+pastureSize+1, playerPosition.x+pastureSize+1, playerPosition.y+wallHeight, playerPosition.z+pastureSize+1, block.GRASS.id)
    mc.setBlocks(playerPosition.x+pastureSize+1, playerPosition.y-1, playerPosition.z+pastureSize+1, playerPosition.x+pastureSize+1, playerPosition.y+wallHeight, playerPosition.z-pastureSize+1, block.GRASS.id)

    mc.player.setTilePos(playerPosition)
