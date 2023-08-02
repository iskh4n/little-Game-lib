import pygame
import random
import math


pygame.init()

screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption("Pygame Calismasi")
icon = pygame.image.load('grim-reaper.png')
pygame.display.set_icon(icon)
background = pygame.image.load('bg1.png')

# ----player
playerImg = pygame.image.load('spaceship.png')
playerX = 350
playerY = 480
playerX_change = 0

# -------------enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies=6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemys (4).png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# -------------bullet
bulletImg = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

player_score=0
score=0

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # iki noktanın mesafesi ve orta noktası
    distance = math.sqrt((math.pow(enemyX - enemyY, 2)) + (math.pow(bulletX - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False
light_grey = (200, 200, 200)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((128, 200, 128))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                print('left')
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                print('right')
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('kaldirildi')
                playerX_change = 0

    # player kenarlar
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # --------------enemy
    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print('SCORE! ', score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)

    # mermi yönü
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        # bullet_state="ready"


    score_text=basic_font.render("SCORE "+ str(score),False,light_grey)

    screen.blit(score_text,(350,10))
    player(playerX, playerY)

    pygame.display.update()
    clock.tick(60)
