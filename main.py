import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# creating a window(screen) for it
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy - array are created for spawning mutplir enemies from 1-6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Enemy.png'))# Holding the enemy png
    enemyX.append(random.randint(0, 736))  # Random x pos
    enemyY.append(random.randint(50, 150)) # Random y pos
    enemyX_change.append(4)   #  enemyY_change.append(40)
    enemyY_change.append(40)  # value used to move Up and Down

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png') # Holding the bullet png
bulletX = 0 # bullet need not want the x position
bulletY = 480 # since the p[layer position is 480
bulletX_change = 0
bulletY_change = 10 # it is going to move with the speed of 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):  # creating a function for importing the player at exact pos
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):   # creating a function for importing the Enemy at exact pos
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y): # creating the function for bullet firing
    global bullet_state # declaring the bullet_state var as global one
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # +16 & +10 is used to shoot the bullet exactly from center of the space ship

#if collision happens
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # calculating distance between midpoint of enemy and midpoint of bullet
    # dist = sqrt of [ (x2-x1)sq + (y2-y1)sq ]
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    #          while True :
    #            R G B
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0)) #(image,(x_pos,y_pos))
    for event in pygame.event.get(): # var = event
        if event.type == pygame.QUIT: # pygame.QUIT = Close Button
            running = False # then return as close so the window get closed

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX  # Get the current x corordinate of the spaceship
                    fire_bullet(bulletX, bulletY)



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # bounding box for player , so that it will not go outside the display
    playerX += playerX_change # adding the incre/decre to the movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy movement (Automatic one)
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i] # adding the incre/decre to the movement
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4 # if it hits rightside adding -4 to turn to right side &
            enemyY[i] += enemyY_change[i]  # and moving downwards with the speed of y

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # if collision = true
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480 # again start from first (loading in the player)
            bullet_state = "ready"
            score_value += 1 # score will be added
            # and after that respawing the enemy , so back to its random line
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # calling the Enemy function

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY) # bullet_position ( x= player's pos , y => reduce as 40)
        bulletY -= bulletY_change

    player(playerX, playerY) # calling the Player function
    show_score(textX, testY)
    pygame.display.update()  # an important default line used to update the display