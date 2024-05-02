import time
import pygame
import sys
import os
import random
import math
from pygame import mixer
# os.environ['QT_QPA_PLATFORM']='xcb'

# initialize the game
pygame.init()

# top-left is origin (0,0)
# top-right is (x_max, 0)
# bottom-left is (0, y_max)
# bottom-right is (x_max, y_max)
# create screen-tuple (width, height)==(x_max, y_max)

# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800,600))

# player
target_size = (64,64)
playerimg = pygame.image.load('spaceship.png')
playerimg = pygame.transform.scale(playerimg, target_size)
player_x = 370      #xcoord of player
player_y = 480      #ycoord of player
px_change = 0

# enemy
enemyimg = []
enemy_x = []
enemy_y = []
ex_change = []
ey_change = []
num_ene = 6
for i in range(num_ene):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemy_x.append(random.randint(0,736))       #xcoord of enemy
    enemy_y.append(random.randint(0,200))       #ycoord of enemy
    ex_change.append(0.3)
    ey_change.append(40)
# print(enemy_x, enemy_y)

# background image
target_sizee = (800, 600)
backimg = pygame.image.load('back.jpg')
backimg = pygame.transform.scale(backimg, target_sizee)

# backgroung sound play
mixer.music.load('background.wav')
mixer.music.play(-1)

# bullet
bulletimg = pygame.image.load('bullet.png')
bullet_x = 0         #xcoord of bullet
bullet_y = 480       #ycoord of bullet
bx_change = 0
by_change = 0.3
bullet_state = 'ready'  #can't see bullet on screen
# fire state of bullet on screen

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y))

def firebull(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x+16, y+10))

def iscollision(ex,ey,bx,by):
    dist = math.sqrt(math.pow(ex-bx, 2) + math.pow(ey-by, 2))
    if dist < 27:
        return True
    return False

def show_score(x,y):
    s = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(s, (x, y))

text_end= pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    s = text_end.render("GAME OVER", True, (255,255,255))
    screen.blit(s, (200,250))

# game loop
running = True
while running:
    # background color
    screen.fill((10,10,10))
    screen.blit(backimg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('byeee')
            running = False
        # if keystroke is pressed check left or right
        if event.type == pygame.KEYDOWN:
            print('keyyyyyyyyyyyyyyyyyyyy')
            if event.key == pygame.K_LEFT:
                print("left arrow pressed")
                px_change = -0.3
            if event.key == pygame.K_RIGHT:
                print("right arrow pressed")
                px_change = 0.3
            if event.key == pygame.K_SPACE:         # fire bullets when space is pressed
                if bullet_state == 'ready':
                    bull_sound = mixer.Sound('laser.wav')
                    bull_sound.play()
                    bullet_x = player_x
                    firebull(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('key released')
                px_change = 0
    player_x = player_x + px_change
    
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    
    for i in range(num_ene):
        enemy_x[i] = enemy_x[i] + ex_change[i]
        if enemy_y[i] >= 440:
            for j in range(num_ene):
                enemy_y[j] = 2000
            game_over()
            break
        if enemy_x[i] <= 0:
            ex_change[i] = 0.3
            enemy_y[i] = enemy_y[i] + ey_change[i]
        elif enemy_x[i] >= 736:
            ex_change[i] = -0.3
            enemy_y[i] = enemy_y[i] + ey_change[i]
        
        # collision detection
        coll = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if coll:
            explo = mixer.Sound('explosion.wav')
            explo.play()
            bullet_y = 480
            bullet_state = 'ready'
            score = score + 1
            print(score)
            enemy_x[i] = random.randint(0,736)       #xcoord of enemy
            enemy_y[i] = random.randint(0,150)       #ycoord of enemy
        enemy(enemy_x[i],enemy_y[i],i)
    
    # bullet movement
    if bullet_state == 'fire':
        firebull(bullet_x, bullet_y)
        bullet_y = bullet_y - by_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'
    
    player(player_x,player_y)
    show_score(textX, textY)
    pygame.display.update()