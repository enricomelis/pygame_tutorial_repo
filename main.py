import pygame
import os

pygame.font.init()
pygame.display.set_caption("First Game!")

# constants zone

# dimensions
WIDTH, HEIGHT = 900, 500
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 50, 40
BULLET_WIDTH = 6
BULLET_HEIGHT = 6
BORDER_WIDTH = 10
BORDER_HEIGHT = HEIGHT
HEALTH_FONT = pygame.font.SysFont('comicsans', 36)
WINNER_FONT = pygame.font.SysFont('comicsans', 72)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# gameplay
FPS = 60
VEL = 4
BULLET_VEL = 6
MAX_BULLTES = 3
HEALTH = 10
DMG = 1
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270)
BORDER = pygame.Rect((WIDTH / 2 - (BORDER_WIDTH//2)), 0, BORDER_WIDTH, BORDER_HEIGHT)


# events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# functions zone

def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > (BORDER.x + BORDER.width): #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #DOWN
        red.y += VEL

def handle_bullets(y_blts, r_blts, y, r):
    for bul in y_blts:
        bul.x += BULLET_VEL
        if r.colliderect(bul): #this works only for 2 rects
            pygame.event.post(pygame.event.Event(RED_HIT))
            y_blts.remove(bul)
        elif bul.x > WIDTH:
            y_blts.remove(bul)

    for bul in r_blts:
        bul.x -= BULLET_VEL
        if y.colliderect(bul): #this works only for 2 rects
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            r_blts.remove(bul)
        elif bul.x < 0:
            r_blts.remove(bul)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(600, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = [] # LEFT-SHIFT = left shooter
    red_bullets = []
    yellow_health = HEALTH
    red_health = HEALTH

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLTES:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, 
                        yellow.y + yellow.height//2 - BULLET_HEIGHT/2, 
                        10, 
                        5
                        )
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLTES:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height//2 - BULLET_HEIGHT/2, 
                        10, 
                        5
                        )
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= DMG

            if event.type == YELLOW_HIT:
                yellow_health -= DMG

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins"
        if red_health <= 0:
            winner_text = "Yellow Wins"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
    
    main()

if __name__ == "__main__":
    main()