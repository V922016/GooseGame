import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, K_w, K_a, K_s, K_d
from pygame.math import Vector2 #Importing vectors for easier work with moving and speed

pygame.init()
infoObject = pygame.display.Info()  # Receiving info about actual screen resolution

# Settings (moving all game settings (like FPS) to the beginning of the file in the form of constants)
FPS = 120
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  # Adopting the game resolution to the current screen resolution
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN) # Setting fullscreen mode for the game
# Game colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
YELLOW_COLOR = (255, 255, 0)
# Player settings
PLAYER_SIZE = Vector2(20, 20) # For more flexible and understandable code
PLAYER_SPEED = Vector2(1, 1)  # Allows you to work more naturally with motion vectors
PLAYER_MOVE_DOWN = [0, 1]
PLAYER_MOVE_UP = [0, -1]
PLAYER_MOVE_LEFT = [-1, 0]
PLAYER_MOVE_RIGHT = [1, 0]

# Creating enemies for player
def create_enemy ():
    ENEMY_SIZE = (30, 30)
    ENEMY = pygame.Surface(ENEMY_SIZE)
    ENEMY.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0,HEIGHT-100), *ENEMY_SIZE)
    enemy_move = [random.randint(-6, -1), 0] # Moving left
    return [ENEMY, enemy_rect, enemy_move]

# Creating bonuses for player
def create_bonus():
    BONUS_SIZE = (20, 20)    
    BONUS = pygame.Surface(BONUS_SIZE)
    BONUS.fill(YELLOW_COLOR)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - BONUS_SIZE[0]), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(1, 3)]  # Moving down
    return [BONUS, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)  # Creating enemy every 1.5 seconds
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)  # Creating bonus every 2 seconds


# Initialization
clock = pygame.time.Clock()
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
player_surface = pygame.Surface(PLAYER_SIZE)
player_surface.fill(COLOR_WHITE)
player_rect = player_surface.get_rect()
player_velocity = PLAYER_SPEED

enemies = []  # Enemies storage
bonuses = []  # Bonuses storage

playing = True
while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Quitting game by pushing Esc
                playing = False
        if event.type == CREATE_ENEMY:  # Creating enemies inside the game
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:  # Creating bonuses inside the game
            bonuses.append(create_bonus())

    main_display.fill(COLOR_BLACK)
    keys=pygame.key.get_pressed()   # Adding using keys
    # Moving player by the keys
    if (keys[K_DOWN] or keys[K_s]) and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(PLAYER_MOVE_DOWN)
    if (keys[K_UP] or keys[K_w]) and player_rect.top > 0:
        player_rect = player_rect.move(PLAYER_MOVE_UP)
    if (keys[K_LEFT] or keys[K_a]) and player_rect.left > 0:
        player_rect = player_rect.move(PLAYER_MOVE_LEFT)
    if (keys[K_RIGHT] or keys[K_d]) and player_rect.right < WIDTH:
        player_rect = player_rect.move(PLAYER_MOVE_RIGHT)

    for enemy in enemies:   # Showing enemies on the screen
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])
    for bonus in bonuses:   # Showing bonuses on the screen
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

    main_display.blit(player_surface, player_rect)    
    pygame.display.flip()

    # Deleting enemies outside the screen
    enemies = [enemy for enemy in enemies if enemy[1].left >= 0]
    # Deleting bonuses outside the screen
    bonuses = [bonus for bonus in bonuses if bonus[1].top <= HEIGHT]