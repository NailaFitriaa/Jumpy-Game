import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy

# initiallize pygame
mixer.init()
pygame.init()

# game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy Game')
icon = pygame.image.load('Jumpy Game/assets/ghost.png')
pygame.display.set_icon(icon)

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# load music and sounds
pygame.mixer.music.load('Jumpy Game/assets/fuyu-biyori bgm.mp3')
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1, 0.0)
jump_fx = pygame.mixer.Sound('Jumpy Game/assets/jump.mp3')
jump_fx.set_volume(1)
death_fx = pygame.mixer.Sound('Jumpy Game/assets/death.mp3')
death_fx.set_volume(1)

# game variable
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else: 
    high_score = 0

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# PANEL = (153, 217, 234) ga jadi

# font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

# load images
jumpy_image = pygame.image.load('Jumpy Game/assets/buddy.png').convert_alpha()
bg_image = pygame.image.load('Jumpy Game/assets/background2.png').convert_alpha()
platform_image = pygame.image.load('Jumpy Game/assets/wood.png').convert_alpha()

# bird spritesheet
bird_sheet_img = pygame.image.load('Jumpy Game/assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)

# function for displaying text to the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# draw panel info
def draw_panel():
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)

# function for drawing bg
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

# player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
    
    def move(self):
        # reset variable
        scroll = 0
        dx = 0
        dy = 0
        
        # process key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = False
        if key[pygame.K_d]:
            dx = 10
            self.flip = True
        
        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        # screen limit for player
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check collosion with platforms
        for platform in platform_group:
            # collosion in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # chech if above platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()

        # check if player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        # update rect position
        self.rect.x += dx
        self.rect.y += dy + scroll

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))   # buat ngeflip gambar sesuai arah move


# platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x, y, width, moving):
       
