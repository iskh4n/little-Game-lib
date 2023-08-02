import pygame
import os

# sabitler

WIDTH = 800
HEIGHT = 640

siyah = (0, 0, 0)
beyaz = (250, 250, 250)

mermihızı = 5


#ekranın istediğin noktada açılış
os.environ['SDL_VIDEO_WINDOW_POS'] = '600, 200'

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
mermiler = []

# pencerenin ortası
center = pygame.math.Vector2(screen.get_rect().center)

# döngü

clock = pygame.time.Clock()

while True:
    screen.fill(siyah)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type== pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                # get vector from center to mouse position
                vector = event.pos - center


                # normalize
                normal = vector.normalize()

                # create speed vector
                speed = normal * mermihızı

                # move object (first move 5 times bigger then next moves )
                pos = center + (speed * 5)

                pygame.draw.line(screen, (255,150,100), pos, center)

                # remeber position and speed as one object
                mermiler.append( [pos, speed] )

    # ekrana yazdırma

    for pos, speed in mermiler:
        # hareket
        pos += speed

        pygame.draw.rect(screen, beyaz, (pos.x, pos.y, 2, 2))

    pygame.display.update()

#fps
    clock.tick(60)

