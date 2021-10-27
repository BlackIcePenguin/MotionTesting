import pygame
import math
import random

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLORS = [RED, GREEN, BLUE, WHITE]

# Create Math Constant
PI = math.pi

# To convert from Degrees to Radians -> angle * (pi / 180)

# Game Constants
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 500
SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
FPS = 60


class Box:
    def __init__(self, display, x, y, width, height, color):
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = 0
        self.y_speed = random.randint(3, 5)
        self.color = color

    def draw_box(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, self.width, self.height], width=0)

    def update(self):
        self.x += self.x_speed
        if self.x + self.width >= DISPLAY_WIDTH:
            self.x = DISPLAY_WIDTH - self.width
        elif self.x <= 0:
            self.x = 0
        self.y += self.y_speed
        if self.y + self.height >= DISPLAY_HEIGHT:
            self.y = DISPLAY_HEIGHT - self.height
        elif self.y <= 0:
            self.y = 0

    def drop_box(self):
        if self.y > DISPLAY_HEIGHT:
            self.x = random.randrange(0, DISPLAY_WIDTH, 5)
            self.y = random.randrange(-100, 0, 5)
            self.y_speed = random.randint(3, 5)
        self.y += self.y_speed

    def reset(self):
        self.x = random.randrange(0, DISPLAY_WIDTH, 5)
        self.y = random.randrange(-100, 0, 5)
        self.y_speed = random.randint(3, 5)

    def is_collided(self, other):
        counter = 0
        for x_val in range(-self.width + 5, self.width - 5):
            if self.x + x_val == other.x:
                for y_val in range(-self.width + 5, self.width - 5):
                    if self.y - y_val == other.y:
                        counter += 1
                        other.reset()
                    else:
                        pass
            else:
                pass
        if counter == 3:
            return True


# --------------------------------------------------------------------------- #
pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Pygame v1')

clock = pygame.time.Clock()

running = True

# Player Creation
player_width = 30
x_loc = (DISPLAY_WIDTH - player_width)/2
y_loc = DISPLAY_HEIGHT - 2*player_width
player = Box(screen, x_loc, y_loc, player_width, player_width, BLACK)

# Enemy Creation
enemy_width = 20
enemy_list = []
for i in range(10):
    x_coord = random.randrange(0, DISPLAY_WIDTH, 5)
    random_y = random.randrange(-100, 0, 5)
    enemy_list.append(Box(screen, x_coord, random_y, enemy_width, enemy_width, RED))
while running:
    # Get all input events (Keyboard, Mouse, Joystick, etc

    # pressed_lft = pygame.mouse.get_pressed()[0]
    # print(pressed_lft)
    pos = pygame.mouse.get_pos()
    # print(pos)
    player.x = pos[0] - .5*player.width
    player.y = pos[1]
    for event in pygame.event.get():

        # Look for specific event
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT:
        #         player.x_speed = 5
        #     if event.key == pygame.K_LEFT:
        #         player.x_speed = -5
        #     if event.key == pygame.K_UP:
        #         player.y_speed = -5
        #     if event.key == pygame.K_DOWN:
        #         player.y_speed = 5
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_RIGHT:
        #         if player.x_speed < 0:
        #             pass
        #         else:
        #             player.x_speed = 0
        #     if event.key == pygame.K_LEFT:
        #         if player.x_speed > 0:
        #             pass
        #         else:
        #             player.x_speed = 0
        #     if event.key == pygame.K_UP:
        #         if player.y_speed > 0:
        #             pass
        #         else:
        #             player.y_speed = 0
        #     if event.key == pygame.K_DOWN:
        #         if player.y_speed < 0:
        #             pass
        #         else:
        #             player.y_speed = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # Game logic (Objects fired, object movement) goes here

    screen.fill(WHITE)

    player.draw_box()
    player.update()
    for enemy in enemy_list:
        enemy.draw_box()
        enemy.drop_box()
        if player.is_collided(enemy):
            running = False

    pygame.display.flip()

    clock.tick(FPS)


# Runs when main game loop ends
pygame.quit()
