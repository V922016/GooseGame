import pygame
import random
import os # For processing system paths
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, K_w, K_a, K_s, K_d
from pygame.math import Vector2 #Importing vectors for easier work with moving and speed

pygame.init()
infoObject = pygame.display.Info()  # Receiving info about actual screen resolution

# Engine settings
# Moving all game settings (like FPS) to the beginning of the file in the form of constants)
FPS = 120
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  # Adopting the game resolution to the current screen resolution
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN) # Setting fullscreen mode for the game
# Game colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
YELLOW_COLOR = (255, 255, 0)
# Game Fonts
FONT = pygame.font.SysFont('Verdana', 40)
# Player settings
PLAYER_SIZE = Vector2(20, 20) # For more flexible and understandable code
PLAYER_SPEED = Vector2(2, 2)  # Allows you to work more naturally with motion vectors
PLAYER_MOVE_DOWN = [0, 4]
PLAYER_MOVE_UP = [0, -4]
PLAYER_MOVE_LEFT = [-4, 0]
PLAYER_MOVE_RIGHT = [4, 0]
# Initializing images (IMPORTANT!!! You have to locate images by the following order: the last layer in the top of the code!)
# The same order for the next layers!
background = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT)) # The last layer, the first in the code!
PLAYER_ANIM_IMAGE_PATH = "banderogoose_anim"    # Here is the path to the player anim images directory
# Loading player anim images and processing alpha channel
PLAYER_ANIM_IMAGES = [pygame.image.load(os.path.join(PLAYER_ANIM_IMAGE_PATH, img)).convert_alpha() for img in sorted(os.listdir(PLAYER_ANIM_IMAGE_PATH))]
player_img = pygame.image.load('player.png').convert_alpha() # Pre-last layer, the second in the code!
enemy_img = pygame.image.load('enemy.png').convert_alpha()  # Pre-last layer
bonus_img = pygame.image.load('bonus.png').convert_alpha()  # Pre-last layer

# Creating enemies for player
def create_enemy ():
    ENEMY_SIZE = (30, 30)
    ENEMY = enemy_img
    enemy_mask = pygame.mask.from_surface(ENEMY)
    # Getting the overall rectangle of the visible part of the image
    if enemy_mask.get_bounding_rects():
        enemy_visible_bounds = enemy_mask.get_bounding_rects()[0]
    else:
        # If it was not possible to get the boundaries, use the default size
        enemy_visible_bounds = pygame.Rect(0, 0, *ENEMY_SIZE)
    # Enemies appear no higher than 1/10 from the top and no lower than 1/4 from the bottom of the screen
    enemy_rect = pygame.Rect(WIDTH - enemy_visible_bounds.width, random.randint(int(HEIGHT / 10), int(HEIGHT - HEIGHT / 4 - enemy_visible_bounds.height)), enemy_visible_bounds.width,
        enemy_visible_bounds.height)
    enemy_move = [random.randint(-8, -4), 0] # Moving left
    return [ENEMY, enemy_rect, enemy_move, enemy_mask]

# Creating bonuses for player
def create_bonus(): 
    BONUS_SIZE = (30, 30) 
    BONUS = pygame.transform.scale(bonus_img, (bonus_img.get_width() // 2, bonus_img.get_height() // 2))
    # Creating a mask from the reduced image to process the visible part
    bonus_mask = pygame.mask.from_surface(BONUS)
    # Getting the overall rectangle of the visible part of the image
    if bonus_mask.get_bounding_rects():
        bonus_visible_bounds = bonus_mask.get_bounding_rects()[0]
    else:
        # If it was not possible to get the boundaries, use the default size
        bonus_visible_bounds = pygame.Rect(0, 0, *BONUS_SIZE)
    # For better picture we're creating bonuses not constantly on the top screen border, but a little upper
    # Subtracting 1/4 of the screen height plus the bonus height for the valid starting position
    initial_position_y = -(HEIGHT / 4 + bonus_visible_bounds.height)
    # Limit the appearance of bonuses, leaving 1/12 of the screen width from the edges
    bonus_rect = pygame.Rect(random.randint(int(WIDTH / 12), int(WIDTH - WIDTH / 12 - bonus_visible_bounds.width)), initial_position_y, bonus_visible_bounds.width,
        bonus_visible_bounds.height)
    bonus_move = [0, random.randint(4, 8)]  # Moving down    
    return [BONUS, bonus_rect, bonus_move, bonus_mask]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)  # Creating enemy every 1.5 seconds
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)  # Creating bonus every 2 seconds
PLAYER_ANIM = pygame.USEREVENT + 3
pygame.time.set_timer(PLAYER_ANIM, 200)  # Animating player every 200 mseconds

# Initialization
clock = pygame.time.Clock()
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
player_surface = player_img
player_rect = player_surface.get_rect()
player_velocity = PLAYER_SPEED
player = [player_img, player_rect, player_velocity]
# Storages
enemies = []  # Enemies storage
bonuses = []  # Bonuses storage
score = 0  # Score storage
player_anim_image_index = 0
# Initializing dynamic game background
background_x1 = 0
background_x2 = background.get_width()
background_move = 3

playing = True
while playing:
    clock.tick(FPS)
    # Обновляем состояние игрока (например, позицию, направление, изображение)
    # Здесь происходит изменение player_surface, если это необходимо
    # player_surface = player_img  # или другое изображение в зависимости от состояния игрока

    # Создаём или обновляем маску игрока на основе текущего изображения
    player_mask = pygame.mask.from_surface(player_surface)

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
        if event.type == PLAYER_ANIM:
            player_surface = PLAYER_ANIM_IMAGES[player_anim_image_index]
            player_anim_image_index += 1
            if player_anim_image_index >= len(PLAYER_ANIM_IMAGES):
                player_anim_image_index = 0
            # Обновляем маску игрока с новым кадром анимации
            player_mask = pygame.mask.from_surface(player_surface)
            player_rect.size = player_surface.get_size()  # Обновляем размер rect, если размеры кадров анимации различаются


    # Adding dynamic background moving
    background_x1 -= background_move
    background_x2 -= background_move
    if background_x1 < -background.get_width():
        background_x1 = background.get_width()
    if background_x2 < -background.get_width():
        background_x2 = background.get_width()
    main_display.blit(background, (background_x1,0))
    main_display.blit(background, (background_x2,0))

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
    
    for enemy in enemies[:]:   # Showing enemies on the screen
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        offset_x = enemy[1].x - player_rect.x
        offset_y = enemy[1].y - player_rect.y       
        if player_mask.overlap(enemy[3], (offset_x, offset_y)): # Descriding behaivor while player impacts with enemy # Используем маски для проверки столкновения
            playing = False
            break
    for bonus in bonuses[:]:   # Showing bonuses on the screen
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1]) 
        offset_x = bonus[1].x - player_rect.x
        offset_y = bonus[1].y - player_rect.y        
        if player_mask.overlap(bonus[3], (offset_x, offset_y)): # Descriding behaivor while player impacts with bonus
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player_surface, player_rect)
       
    pygame.display.flip()

    # Deleting enemies outside the screen
    enemies = [enemy for enemy in enemies if enemy[1].right > -WIDTH / 10]  # For better picture we're deleting enemies not constantly on the screen border
    # Deleting bonuses outside the screen
    bonuses = [bonus for bonus in bonuses if bonus[1].top <= HEIGHT]

    # Printing to the console quantity of active enemies and bonuses (for debugging, no decomment without necessity)
    #print("Количество активных врагов:", len(enemies))
    #print("Количество активных бонусов:", len(bonuses))

    pygame.display.update()