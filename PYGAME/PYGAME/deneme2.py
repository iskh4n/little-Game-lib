import pygame, sys, random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # oyuncu skoru hesaplama
    if ball.left <= 0:
        score_time = pygame.time.get_ticks()
        player_score += 1

    # ai skoru hesaplama
    if ball.right >= screen_width:
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_start():
    global ball_speed_x, ball_speed_y, ball_moving, score_time

    ball.center = (screen_width / 2, screen_height / 2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = basic_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = basic_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = basic_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


# Genel yüklemeler
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

#pencere
screen_width = 800
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# renkler
light_grey = (200, 200, 200)
white=(255,255,255)
green=(51, 255, 82)
red=(199, 0, 57)
bg_color = pygame.Color('cornsilk4')
coral=pygame.Color('coral4')

# dörtgenler
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20 - 15, screen_height / 2 - 70, 10 + 300, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# değişkenler
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True

# score yazısı
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 10
            if event.key == pygame.K_DOWN:
                player_speed += 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 10
            if event.key == pygame.K_DOWN:
                player_speed -= 10

    # oyun işleyişi
    ball_animation()
    player_animation()
    opponent_ai()

    screen.fill(bg_color)
    pygame.draw.rect(screen, green, player)
    pygame.draw.rect(screen, red, opponent)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen,coral , (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time:
        ball_start()

    player_text = basic_font.render(f'{player_score}', False, green)
    screen.blit(player_text, (410, 30))

    opponent_text = basic_font.render(f'{opponent_score}', False, red)
    screen.blit(opponent_text, (375, 30))
    score_text=basic_font.render("SCORE",False,light_grey)
    screen.blit(score_text,(350,1))
    pygame.display.flip()
    clock.tick(60)