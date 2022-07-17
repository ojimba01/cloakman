# All Imports
#-------------------------------------------------------------------------------
import pygame
import random
from pygame.locals import *
import sys
from config import *
from blocks import blocks
from player import player as p
from  movement import move
from sprites import *
from load import map
import entity as e
#-------------------------------------------------------------------------------

#Clock Configuration
#-------------------------------------------------------------------------------
clock = pygame.time.Clock()
#-------------------------------------------------------------------------------

#Pygame Initialization
#-------------------------------------------------------------------------------
pygame.init()
pygame.display.set_caption("CloackMan")
#-------------------------------------------------------------------------------

#Window Size
#-------------------------------------------------------------------------------
WINDOW_SIZE = (WIN_WIDTH, WIN_HEIGHT)
#-------------------------------------------------------------------------------

#Data Retrieval
#-------------------------------------------------------------------------------
positions = []
true_scroll = [0,0]
jumper_objects = []
animation_database = {}
#-------------------------------------------------------------------------------

#Block Configuration
#-------------------------------------------------------------------------------
grass=blocks.transformsprites("blocks/tile001.png")
dirt=blocks.transformsprites("blocks/tile013.png")
#-------------------------------------------------------------------------------
jumpy = blocks.transformsprites2("jumper.png")
jumpy.set_colorkey((255,255,255))
#-------------------------------------------------------------------------------

#Screen Configuration
#-------------------------------------------------------------------------------
scene = pygame.image.load("spritesheets/background/background.png")
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((320, 140))
true_display=pygame.transform.scale(display, WINDOW_SIZE)
font = pygame.font.SysFont(None, 24)
screen.blit(true_display, (0,0))
# **scaling the display to window size
true_scene=pygame.transform.scale(scene, BACKGROUND)
tilemap = map.load_map('tilemap')
#-------------------------------------------------------------------------------

#Initialize the player and other objects
#-------------------------------------------------------------------------------
rect = pygame.Rect(100,100,32,32)
p1 = p(rect)
jumper = e.entity((random.randint(100,160),250), jumpy)
for i in range(1):
    jumper_objects.append(jumper)
mjumper = e.entitym()
#-------------------------------------------------------------------------------

#Loading the spritesheets for Player and Enemies
#-------------------------------------------------------------------------------
animation_database['run'] = sprites.load_animation('player_animations/run',[7,7,7,7,7,7])
animation_database['idle'] = sprites.load_animation('player_animations/idle',[7,7,7,7])
animation_database['jump'] = sprites.load_animation('player_animations/jump',[4,4,4])
animation_database['jumpdown'] = sprites.load_animation('player_animations/jumpdown',[4,4,4])
#-------------------------------------------------------------------------------

#Retrievess the mouse cursor position
#function that displays the mouse's position on the screen
#-------------------------------------------------------------------------------
def mouse_pos():
    x1,y1 = pygame.mouse.get_pos()
    xm = int((pygame.mouse.get_pos()[0])+true_scroll[0])
    ym = int((pygame.mouse.get_pos()[1])+true_scroll[1])
    x = f"X: {xm}"
    y = f"Y: {ym}"
    xt = font.render(f'{x}', True, pygame.Color('black'))
    yt = font.render(f'{y}', True, pygame.Color('Black'))
    screen.blit(xt, (len(x), 10))
    screen.blit(yt, (len(y), 30))
    pygame.draw.circle(screen, (255,0,0), (x1,y1), 3)
    return xm,ym
#Returns the X and Y position of the mouse cursor in relation to game "screen"
#and not the game window.
#-------------------------------------------------------------------------------

#Game Loop
while True:
    screen.blit(true_scene, (0,-480))
    tile_rects = []
    mouse_pos()
# Below is the scrolling feaature within the game that allows the screen to essentially follow the p1.player.
    true_scroll[0] += (p1.player_rect.x-true_scroll[0]-222)/20
    true_scroll[1] += (p1.player_rect.y-true_scroll[1]-212)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    y = 0
# Populates the tiles with the correct images on to the screen in occordance with the tilemap.
    for row in tilemap:
        x = 0
        for tile in row:
            if tile == '2':
                screen.blit(grass, (x * TILE_SIZE - true_scroll[0], y * TILE_SIZE - true_scroll[1]))
            if tile == '1':
                screen.blit(dirt, (x * TILE_SIZE - true_scroll[0], y * TILE_SIZE - true_scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    
# This is the coordinate/movement detection for the player [0,1]=[x,y].
    p1.player_movement = [0,0]
    if p1.moving_right == True:
        p1.player_movement[0] += 4
    if p1.moving_left == True:
        p1.player_movement[0] -= 4
    p1.player_movement[1] += p1.vertical_momentum
    p1.vertical_momentum += 0.2
    if p1.vertical_momentum > 4:
        p1.vertical_momentum = 4

# This is the key & direction detection for the sprite's frame.
    if p1.player_movement[0] == 0:
        
        p1.player_action,p1.player_frame = sprites.change_action(p1.player_action,p1.player_frame,'idle')
    if p1.player_movement[0] > 0 and collisions['bottom']==True:
        p1.player_flip_x = False
        p1.player_action,p1.player_frame = sprites.change_action(p1.player_action,p1.player_frame,'run')
    if p1.player_movement[0] < 0 and collisions['bottom']==True:
        p1.player_flip_x = True
        p1.player_action,p1.player_frame = sprites.change_action(p1.player_action,p1.player_frame,'run')
    if p1.player_movement[0] > 0:
        if p1.vertical_momentum < 0 :
            p1.player_flip_x = False
            p1.player_action,p1.player_frame = sprites.change_action(p1.player_action,p1.player_frame,'jump')
    if p1.player_movement[0] < 0:
        if p1.vertical_momentum < 0 :
            p1.player_flip_x = True
            p1.player_action,p1.player_frame = sprites.change_action(p1.player_action,p1.player_frame,'jump')
    p1.player_rect,collisions = move(p1.player_rect, p1.player_movement, tile_rects)

    if collisions['bottom']:
        p1.air_timer = 0
        p1.vertical_momentum = 0
        p1.jumping = False
    else:
        p1.air_timer += 1
    
    p1.player_frame += 1
    
    if p1.player_frame >= len(animation_database[p1.player_action]):
        p1.player_frame = 0
    p1.player_img_id = animation_database[p1.player_action][p1.player_frame]
    p1.player = animation_frames[p1.player_img_id]
    screen.blit(pygame.transform.flip(p1.player,p1.player_flip_x,p1.player_flip_y),(p1.player_rect.x-scroll[0],p1.player_rect.y-scroll[1]))

    for jump in jumper_objects:
        jumper.render(screen,scroll)
        if jumper.collision_test(p1.player_rect):
            p1.vertical_momentum = -8  

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            posi=(event.pos[0]+scroll[0],event.pos[1]+scroll[1])
            positions.append(posi)
            print(event.pos[0]+scroll[0],event.pos[1]+scroll[1])
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                p1.moving_right = True
            if event.key == K_LEFT:
                p1.moving_left = True
            if event.key == K_UP:
                if (p1.air_timer < 6):
                    p1.jumping=True
                    p1.falling=False
                    p1.vertical_momentum = -6
                    p1.player_movement[1] = -5.2
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                p1.moving_right = False
            if event.key == K_LEFT:
                p1.moving_left = False
            if event.key == K_UP:
                p1.jumping = False
    for posi in positions:
        mjumper.render(screen,scroll,jumpy,posi)
        if mjumper.collision_test(p1.player_rect):
            p1.vertical_momentum = -8


    pygame.display.update()
    clock.tick(60)
