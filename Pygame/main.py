import math
import pygame
import random
from pygame import mixer

#initiallize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('op.png')
pygame.display.set_icon(icon)

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Background
background = pygame.image.load('space.jpg')

#Score
Score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#Player
PlayerX = 370
PlayerY = 480
PlayerImg = pygame.image.load('space-invaders.png')
PlayerX_change = 0

#Enemy
EnemyX = []
EnemyY = []
EnemyImg = []
EnemyX_change = []
EnemyY_change = []
nums_of_enemies = 6
for i in range(nums_of_enemies):
    EnemyX.append(random.randint(0,735))
    EnemyY.append(random.randint(50,300))
    EnemyImg.append(pygame.image.load('alien.png'))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)

#Bullet
BulletX = 0
BulletY = 480
BulletImg = pygame.image.load('bullet.png')
BulletX_change = 0
BulletY_change = 0.5
BulletState = 'ready'

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,215,0))
    screen.blit(game_over_text,(200,250))

def show_score(x,y):
    score = font.render("Score : " + str(Score_value), True, (255,215,0))
    screen.blit(score,(x,y))

def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2)+math.pow(EnemyY - BulletY, 2))
    if distance <= 27 :
        return True
    else :
        return False

def player(x,y):
    screen.blit(PlayerImg, (x,y))

def enemy(x,y,i):
    screen.blit(EnemyImg[i], (x,y))

def fire_bullet(x,y):
    mixer.music.load('laser.wav')
    mixer.music.play()
    global BulletState
    BulletState = 'fire'
    screen.blit(BulletImg, (x+16,y+10))

#game loop
running = True

while running:
    #RGB = Red, Green, Blue
    screen.fill((0,0,0))
    
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if BulletState is 'ready':
                    fire_bullet(PlayerX,BulletY)
                    BulletX = PlayerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
    
    PlayerX += PlayerX_change

    if PlayerX <= 0:
        PlayerX = 0
    if PlayerX >= 736:
        PlayerX = 736
    
    # Enemy Movement
    for i in range(nums_of_enemies):

        #Game Over Condition
        if EnemyY[i] > 400 :
            for j in range(nums_of_enemies):
                EnemyY[j] = 2000
            show_game_over()
            break

        EnemyX[i] += EnemyX_change[i]
        
        
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.3
            EnemyY[i] += EnemyY_change[i]
        if EnemyX[i] >= 736:
            EnemyX_change[i] = -0.3
            EnemyY[i] += EnemyY_change[i]
        #Collision
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision :
            mixer.music.load('explosion.wav')
            mixer.music.play()
            BulletY = 480
            BulletState = 'ready'
            Score_value += 1
            EnemyX[i] = random.randint(0,735)
            EnemyY[i] = random.randint(50,300)
        
        enemy(EnemyX[i],EnemyY[i],i)
            
    #Bullet movement
    if BulletY <= 0:
        BulletY = 480
        BulletState = 'ready'

    if BulletState is 'fire':
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change


    player(PlayerX,PlayerY)
    show_score(textX, textY)
    pygame.display.update()