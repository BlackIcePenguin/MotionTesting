import pygame
import math
import random

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (11, 46, 2)
BROWN = (41, 21, 2)
YELLOW = (239, 184, 16)
MAGENTA = (204, 0, 153)
LIGHT_BROWN = (153, 102, 34)
SKY_BLUE = (179, 255, 255)
OCEAN_BLUE = (26, 117, 255)
PEACH = (255, 204, 153)
COLORS = [RED, GREEN, BLUE, WHITE]

# Create Math Constant
PI = math.pi

# To convert from Degrees to Radians -> angle * (pi / 180)

# Game Constants
SIZE = (700, 500)
FPS = 60
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
# --------------------------------------------------------------------------- #
pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Pygame Lab')
FONT = pygame.font.SysFont('Calibri', 25, True, False)

clock = pygame.time.Clock()

running = True


# Setting up the classes
class Person:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.y_speed = 0

    def draw_person_on_raft(self):
        pygame.draw.line(screen, self.color, (self.x + 68, self.y + 10), (self.x + 75, self.y + 35), 2)
        pygame.draw.line(screen, self.color, (self.x + 68, self.y + 10), (self.x + 61, self.y + 35), 2)
        pygame.draw.line(screen, self.color, (self.x + 68, self.y + 10), (self.x + 68, self.y - 15), 2)
        pygame.draw.line(screen, self.color, (self.x + 68, self.y - 10), (self.x + 50, self.y), 2)
        pygame.draw.circle(screen, self.color, (self.x + 69, self.y - 23), 8, width=0)
        pygame.draw.line(screen, self.color, (self.x + 68, self.y - 10), (self.x + 82, self.y - 22), 2)
        pygame.draw.arc(screen, RED, [self.x + 60, self.y - 30, 16, 8], 0, PI, 50)
        pygame.draw.line(screen, self.color, (self.x + 75, self.y - 30), (self.x + 82, self.y - 22), 2)

    def person_move(self):
        self.y += self.y_speed
        if self.y + 72 >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - 72
        elif self.y <= 250:
            self.y = 250


class Raft:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_speed = 0

    def raft_draw(self):
        pygame.draw.rect(screen, BROWN, [self.x, self.y, 100, 72])
        pygame.draw.line(screen, LIGHT_BROWN, (self.x, self.y + 22), (self.x + 99, self.y + 22), 2)
        pygame.draw.line(screen, LIGHT_BROWN, (self.x, self.y + 48), (self.x + 99, self.y + 48), 2)
        pygame.draw.line(screen, LIGHT_BROWN, (self.x + 50, self.y + 36), (self.x + 50, self.y - 72), 5)
        pygame.draw.line(screen, LIGHT_BROWN, (self.x + 28, self.y + 10), (self.x + 70, self.y - 52), 5)
        pygame.draw.arc(screen, BLUE, [self.x + 24, self.y - 40, 15, 50], -PI/2, PI/2, 2)
        # pygame.draw.arc(screen, BLUE, [self.x + 64, self.y - 100, 15, 50], -PI / 2, PI / 2, 2)
        for num in range(0, 50):
            pygame.draw.arc(screen, BLUE, [self.x + 24 + (0.8 * num), self.y - 40 - (1.2 * num), 15, 50],
                            -PI / 2, PI / 2, 2)
        pygame.draw.line(screen, LIGHT_BROWN, (self.x + 28, self.y - 40), (self.x + 70, self.y - 100), 5)

    def raft_move(self):
        self.y += self.y_speed
        # For a 250 top movement bound, more general version in box class
        if self.y + 72 >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - 72
        elif self.y <= 250:
            self.y = 250


class Ocean:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flow_rate = 5
        self.flow_change = 0.1
        self.flow_x = x

    def flow(self):
        for val in range(-15,  18):
            pygame.draw.ellipse(screen, OCEAN_BLUE, [self.flow_x-(40*val), self.y-5, 60, 20])
        self.flow_x += self.flow_rate
        self.flow_rate -= self.flow_change
        if abs(self.flow_rate) >= 5:
            self.flow_change = -1 * self.flow_change

    def main_ocean(self):
        pygame.draw.rect(screen, OCEAN_BLUE, [0, self.y, SCREEN_WIDTH, SCREEN_HEIGHT])


class Sky:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cloud_shift = 1.5

    def cloud(self):
        for value in range(0, 3):
            pygame.draw.ellipse(screen, WHITE, [self.x + (320 * value), self.y, 100, 30])
            pygame.draw.ellipse(screen, WHITE, [self.x + 30 + (320 * value), self.y - 15, 60, 40])
            pygame.draw.ellipse(screen, WHITE, [self.x + 40 + (320 * value), self.y + 10, 80, 35])
        self.x -= self.cloud_shift
        if self.x <= -160:
            self.x += 320

    @staticmethod
    def sun():
        pygame.draw.circle(screen, YELLOW, (0, 0), 89)


class Box:
    def __init__(self, display, x, y, width, height, color):
        self.display = display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_speed = random.randint(3, 5)
        self.y_speed = 0
        self.color = color

    def draw_box(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, self.width, self.height], width=0)

    def draw_triangle(self):
        pygame.draw.polygon(self.display, WHITE, [(self.x + 2, self.y), (self.x + self.width, self.y + self.height),
                                                  (self.x, self.y + self.height)], 0)

    def update(self):
        self.y += self.y_speed
        if self.y + self.height >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
        elif self.y <= 250:
            self.y = 250

    def move_box(self):
        if self.x < 0:
            self.y = random.randrange(250, SCREEN_HEIGHT, 25)
            self.x = random.randrange(700, 800, 15)
            self.x_speed = random.randint(1, 3)
        self.x -= self.x_speed

    def reset(self):
        self.y = random.randrange(250, SCREEN_HEIGHT, 25)
        self.x = random.randrange(700, 800, 15)
        self.y_speed = random.randint(1, 5)

    def is_collided(self, other):
        for x_val in range(-self.width + 5, self.width - 5):
            if self.x + x_val == other.x:
                for y_val in range(-self.height, 20):
                    if self.y - y_val == other.y:
                        other.reset()
                        return True
                    else:
                        pass
            else:
                pass


class Score:
    def __init__(self, display):
        self.display = display

    def draw_score(self, value):
        score_value = FONT.render(f'Fish Caught : {value}', True, BLACK)
        self.display.blit(score_value, [540, 10])

    def draw_timer(self):
        time_text = FONT.render(f'Time taken : {int(time_count)}', True, BLACK)
        self.display.blit(time_text, [540, 60])


class EndScreen:
    def __init__(self, display, x, y, color):
        self.display = display
        self.x = x
        self.y = y
        self.color = color

    def game_end(self):
        end_text = FONT.render(f'You caught 100 fish in {int(time_count)} seconds, good job!', True, WHITE)
        self.display.fill(self.color)
        self.display.blit(end_text, [self.x, self.y])


person = Person(100, 300, PEACH)
raft = Raft(100, 300)
ocean = Ocean(500, 250)
sky = Sky(300, 100)
fish_caught = Score(screen)
player_width = 100
player_height = 72
player = Box(screen, raft.x, raft.y, player_width, player_height, BLACK)
enemy_width = 20
enemy_list = []
counter = 0
time_count = 0
end = EndScreen(screen, 130, 240, OCEAN_BLUE)
at_end = False
for i in range(15):
    y_coord = random.randrange(250, SCREEN_HEIGHT, 15)
    random_x = random.randrange(700, 900, 5)
    enemy_list.append(Box(screen, random_x, y_coord, enemy_width, enemy_width, OCEAN_BLUE))
while running:
    # Get all input events (Keyboard, Mouse, Joystick, etc
    time_count += (1/60)
    for event in pygame.event.get():

        # Look for specific event
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                raft.y_speed = -2
                person.y_speed = -2
                player.y_speed = -2
            if event.key == pygame.K_DOWN:
                raft.y_speed = 2
                person.y_speed = 2
                player.y_speed = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if raft.y_speed > 0:
                    pass
                else:
                    raft.y_speed = 0
                    person.y_speed = 0
                    player.y_speed = 0
            if event.key == pygame.K_DOWN:
                if raft.y_speed < 0:
                    pass
                else:
                    raft.y_speed = 0
                    person.y_speed = 0
                    player.y_speed = 0

    screen.fill(SKY_BLUE)
    ocean.main_ocean()
    ocean.flow()
    sky.sun()
    sky.cloud()
    player.update()
    raft.raft_move()
    player.draw_box()
    raft.raft_draw()
    person.person_move()
    person.draw_person_on_raft()
    for enemy in enemy_list:
        enemy.draw_box()
        enemy.draw_triangle()
        enemy.move_box()
        if player.is_collided(enemy):
            counter += 1
    fish_caught.draw_score(counter)
    fish_caught.draw_timer()
    if counter >= 100:
        end.game_end()
        pygame.display.flip()
        at_end = True
        running = False

    pygame.display.flip()

    clock.tick(FPS)

if at_end:
    end_clock = 0
    while end_clock < 10000:
        end_clock += 0.0005

# Runs when main game loop ends
pygame.quit()
