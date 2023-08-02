import pygame
from pygame.locals import *
import random


pygame.init()
clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 950
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy deneme')
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)
#değişkenler
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milisaniye
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
#resimler
bg = pygame.image.load('flapp/img/sky1.png')
ground_img = pygame.image.load('flapp/img/ground.png')
button_img = pygame.image.load('flapp/img/restart.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'flapp/img/player{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            #çekim
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            #zıplama
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #animasyon
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #uzaylıyı döndürme
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('flapp/img/pipe.png')
        self.rect = self.image.get_rect()
        #ayna görünümü flip
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False

        #mouse konumu
        pos = pygame.mouse.get_pos()
        #mouse butona gelince
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #buton ciz
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

alien_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Alien(100, int(screen_height / 2))
alien_group.add(flappy)
#restart butonu
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)
run = True
while run:
    clock.tick(fps)
    #arkaplan ve zemin
    screen.blit(bg, (0,0))
    alien_group.draw(screen)
    alien_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll, 800))
    #skor kontrol
    if len(pipe_group) > 0:
        if alien_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and alien_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if alien_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #çarpışma
    if pygame.sprite.groupcollide(alien_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #zemine çarpma
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    if game_over == False and flying == True:

        #süreye bağlı yeni borular yaratma_frequency =1500 ms
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        #sonsuz devam
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()


    #oyun bitti mi
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()