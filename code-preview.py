import pygame
import os
import time
pygame.font.init()

bullets_vel = 10
color = (0, 0, 0)
white = (255,255,255)
red = (255, 0, 0)
yellow = (255, 255, 0)

health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

fps = 60
vel = 8
ship_h = 70
ship_w = 80
max_bullets = 5

width, height = (1280, 720)
border = pygame.Rect(width//2 -5, 0, 15, height)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ruan se Game")
ship_one = pygame.image.load(os.path.join("Assets", "ship.png"))
ship_one = pygame.transform.scale(ship_one, (ship_h, ship_w))
ship_one = pygame.transform.rotate(pygame.transform.scale(ship_one, (ship_h, ship_w)),90)

ship_two = pygame.image.load(os.path.join("Assets", "ship.png"))
ship_two = pygame.transform.scale(ship_two, (ship_h, ship_w))
ship_two = pygame.transform.rotate(pygame.transform.scale(ship_two, (ship_h, ship_w)),270)

two_hit = pygame.USEREVENT + 1
one_hit = pygame.USEREVENT + 2



def arrow_movement(one):
    keys_press = pygame.key.get_pressed()
    if keys_press[pygame.K_LEFT] and one.x - vel > border.x + border.width:  # left key
        one.x -= vel
    if keys_press[pygame.K_RIGHT] and one.x + vel + one.width < width:  # right
        one.x += vel
    if keys_press[pygame.K_UP] and one.y - vel > 0:  # up
        one.y -= vel
    if keys_press[pygame.K_DOWN] and one.y + vel + one.height < height:  # down
        one.y += vel


def dwas_movement(two):
    keys_press = pygame.key.get_pressed()
    if keys_press[pygame.K_a] and two.x - vel > 0:  # left key
        two.x -= vel
    if keys_press[pygame.K_d] and two.x + vel + two.width < border.x:  # right
        two.x += vel
    if keys_press[pygame.K_w] and two.y - vel > 0:  # up
        two.y -= vel
    if keys_press[pygame.K_s] and two.y + vel + two.height < height:  # down
       two.y += vel


def bullets_movemnt(two_bullets, one_bullets, two, one):
    for bullet in two_bullets:
        bullet.x += bullets_vel
        if one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(one_hit))
            two_bullets.remove(bullet)
        elif bullet.x > width:
            two_bullets.remove(bullet)

    for bullet in one_bullets:
        bullet.x -= bullets_vel
        if two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(two_hit))
            one_bullets.remove(bullet)
        elif bullet.x < 0:
            one_bullets.remove(bullet)

def draw_window(one, two, one_bullets, two_bullets, one_health, two_health):
    window.fill(color)
    pygame.draw.rect(window, white, border)
    window.blit(ship_one, (one.x, one.y))
    window.blit(ship_two, (two.x, two.y))

    one_health_text = health_font.render(f"Health: {str(one_health)}", 1, white)
    two_health_text = health_font.render(f"Health: {str(two_health)}", 1, white)
    window.blit(one_health_text, (width - one_health_text.get_width()-10, 10))
    window.blit(two_health_text, (10, 10))

    for bullet in one_bullets:
        pygame.draw.rect(window, red, bullet)

    for bullet in two_bullets:
        pygame.draw.rect(window, yellow, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    window.blit(draw_text, (width//2 - draw_text.get_width()//2, height//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)
def main():
    one = pygame.Rect(1000, 300, ship_w, ship_h)
    two = pygame.Rect(200, 300, ship_w, ship_h)

    one_health = 5
    two_health = 5

    one_bullets = []
    two_bullets = []

    run = True
    clock = pygame.time.Clock()
    #GameLoop
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(two_bullets) < max_bullets:
                    bullet = pygame.Rect(two.x + two.width, two.y + two.height//2 -2, 10 ,5)
                    two_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(one_bullets) < max_bullets:
                    bullet = pygame.Rect(one.x , one.y + one.height//2 -2, 10 ,5)
                    one_bullets.append(bullet)

            if event.type == one_hit:
                one_health -= 1

            if event.type == two_hit:
                two_health -= 1

        winner_text = ""
        if one_health <= 0 :
            winner_text = "Player two wins"
        if two_health <= 0:
            winner_text = "Player one wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        arrow_movement(one)
        dwas_movement(two)
        
        bullets_movemnt(two_bullets, one_bullets, two, one)

        draw_window(one, two, one_bullets, two_bullets, one_health, two_health)
    main()


#Change name here
if __name__ == "__code-preview__":
    main()
