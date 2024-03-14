import pygame
from pygame.constants import QUIT
from pygame.math import Vector2 #Importing vectors for easier work with moving and speed

pygame.init()

# Settings (moving all game settings (like FPS) to the beginning of the file in the form of constants)
FPS = 1200
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
PLAYER_SIZE = Vector2(20, 20) # For more flexible and understandable code
PLAYER_SPEED = Vector2(1, 1)  # Allows you to work more naturally with motion vectors

# Initialization
clock = pygame.time.Clock()
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
player_surface = pygame.Surface(PLAYER_SIZE)
player_surface.fill(COLOR_WHITE)
player_rect = player_surface.get_rect()
player_velocity = PLAYER_SPEED

# Setting collision processing like a function to improve readability and simplify code reuse
# Allows you to simplify the core game loop by focusing on collision logic in one place
def handle_collision_with_bounds(rect, velocity):
    if rect.bottom >= HEIGHT or rect.top <= 0:
        velocity.y = -velocity.y
    if rect.right >= WIDTH or rect.left <= 0:
        velocity.x = -velocity.x

    rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Limits rect to the screen rectangle

playing = True
while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

    main_display.fill(COLOR_BLACK)
    handle_collision_with_bounds(player_rect, player_velocity)
    player_rect.move_ip(player_velocity)
    main_display.blit(player_surface, player_rect)
    pygame.display.flip()