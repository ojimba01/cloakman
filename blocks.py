import pygame
from pygame.locals import *
from config import *
class blocks(object):
    def __init__(self):
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Used for 32x32 sprites
    def transformsprites(filename):
        transform = pygame.image.load(filename)
        fulltransform = pygame.transform.scale(transform, (32,32)) 
        return fulltransform
#-----------------------------------------------------------------------------------------------------------------------
# Used for 16x16 sprites
    def transformsprites2(filename):
        transform = pygame.image.load(filename)
        fulltransform = pygame.transform.scale(transform, (16,16)) 
        return fulltransform