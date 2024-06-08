import pygame
import math


WIDTH = 1000
HEIGHT = 600
FPS = 60

BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RADIUS = 10
gravity = 0.04
ball_moving = False
num_bounces = 0

# Default ball settings
BALL_X = RADIUS * 2
BALL_Y = HEIGHT - (RADIUS * 1)
BALL_Y_CHANGE = -2
BALL_X_CHANGE = 2

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idealistic case projectile motion simulator")

running = True
clock = pygame.time.Clock()
while running:
    screen.fill((BG_COLOR))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Restricting the mouse motion to set a cap on the maximum velocity
    if (mouse_x > BALL_X + 30) and not ball_moving:
        pygame.mouse.set_pos([BALL_X + 30, mouse_y])
    if (mouse_y < BALL_Y - 30) and not ball_moving:
        pygame.mouse.set_pos([mouse_x, BALL_Y - 30])
    
    # Main Logic of velocity calculations and projectile mapping
    if not ball_moving:
        line = pygame.draw.line(screen, RED, [BALL_X, BALL_Y], [mouse_x, mouse_y], 4)
        vel_x = abs(mouse_x - BALL_X)
        vel_y = abs(mouse_y - BALL_Y)
        BALL_X_CHANGE = vel_x / 10
        BALL_Y_CHANGE = -vel_y / 10
        vel = ((vel_x ** 2) +  (vel_y ** 2)) ** 0.5
        theta = math.asin(vel_y / vel)
        max_dist_x = (2 * ((vel/10) ** 2) * math.cos(theta) * math.sin(theta)) / (gravity)
        max_height = ((vel / 10) ** 2 * (math.sin(theta)) ** 2) / (2 * gravity)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_moving = True
                 
    ball = pygame.draw.circle(screen, BLACK, [BALL_X, BALL_Y], RADIUS) 
    
    # Boundary Checking
    if BALL_Y > HEIGHT - RADIUS and not ball_moving:
        BALL_Y = HEIGHT - RADIUS
        BALL_Y_CHANGE = 0
        BALL_X_CHANGE = 0

    if BALL_Y > HEIGHT - RADIUS and ball_moving:
        # Rebounding the ball forwards but coefficient is < 1 in order to disipate energy
        if num_bounces <= 3:
            BALL_Y_CHANGE *= -0.7
            BALL_X_CHANGE *= 0.7
        else:
            BALL_Y_CHANGE = 0
            BALL_X_CHANGE = 0
            BALL_Y = HEIGHT - RADIUS
            ball_moving = False
            num_bounces = 0

        num_bounces += 1
                

    if ball_moving: 
        BALL_Y += BALL_Y_CHANGE 
        BALL_Y_CHANGE += gravity
        BALL_X += BALL_X_CHANGE

        # Drawing a vector representing the ball's velocity
        x_vel_vec = pygame.draw.line(screen, RED, [BALL_X, BALL_Y], [BALL_X + (BALL_X_CHANGE * 10), BALL_Y], 4)
        y_vel_vec = pygame.draw.line(screen, RED, [BALL_X, BALL_Y], [BALL_X, BALL_Y + (BALL_Y_CHANGE * 10)], 4)


    clock.tick(FPS)
    pygame.display.update()
