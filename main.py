# Import libraries
import pygame
import random
import math
from pygame import mixer

# Initializate pygame
pygame.init()

# Window size
screen_width = 800
screen_height = 600

# size variable
size = (screen_width, screen_height)

# Display window
screen = pygame.display.set_mode(size)

# Background image
background = pygame.image.load("Background.png")

# Background music
mixer.music.load("GameMusic.wav")
mixer.music.play(-1)

# Title
pygame.display.set_caption("Space Invaders")

# Icon
icon = pygame.image.load("Alien.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy (Alien)
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

# Number of enemies
number_enemies = 9

# Create multiple enemies
for item in range(number_enemies):
    enemy_img.append(pygame.image.load("Alien.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 130))
    enemy_x_change.append(4)
    enemy_y_change.append(32)

# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 14
bullet_state = "ready"

# Score
score = 0

# Font variable
score_font = pygame.font.Font("Stocky-lx5.ttf", 32)

# text position
text_x = 10
text_y = 10


# Game over text
go_font = pygame.font.Font("Stocky-lx5.ttf", 64)
go_x = 200
go_y = 250

# Game over function
def game_over(x, y):
    go_text = go_font.render("Game Over", True, (255, 255, 255))
    screen.blit(go_text, (x, y))

# score text funcion
def show_text(x, y):
    score_text = score_font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

# Player function
def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy function
def enemy(x, y, item):
    screen.blit(enemy_img[item], (x, y)) 

# Fire Function
def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Colision function
def is_colision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystrokes is pressed
        # checks wheater its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5 

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Explosion.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                fire(player_x, bullet_y)

        # review if keystrokes was relased
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Color RGB: Red - Green - Blue
    rgb = (255, 255, 255)
    screen.fill(rgb)

    # Show background image
    screen.blit(background, (0, 0))

    # Call player function
    player_x += player_x_change
    player(player_x, player_y, )

    # Call enemy function
    enemy(enemy_x[item], enemy_y[item], item)

    # player x boundaries left and right
    if player_x <= 0:
        player_x = 0    

    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    for item in range(number_enemies):
        
        # Game over zone
        if enemy_y[item] > 440:
            for j in range(number_enemies):
                enemy_y[ j ] = 2000

                mixer.music.stop()
                mixer.Sound("GameOver.wav")
            # Call game over function
            game_over(go_x, go_y)

            break
        enemy_x[item] += enemy_x_change[item]
        if enemy_x[item] <= 0:
            enemy_x_change[item] = 4
            enemy_y[item] += enemy_y_change[item]

        elif enemy_x[item] >= 736:
            enemy_x_change[item] = -4
            enemy_y[item] += enemy_y_change[item]

        # Call colision function
        colision = is_colision(enemy_x[item], enemy_y[item], bullet_x, bullet_y)

        if colision:
            explosion_sound =mixer.Sound("invaderkilled.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            # print(score)
            enemy_x[item] = random.randint(0, 735)
            enemy_y[item] = random.randint(50, 130)
        
        # Call enemy function
        enemy(enemy_x[item], enemy_y[item], item)
    
    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    
    if bullet_state == "fire":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Call the text function
    show_text(text_x, text_y)

    # Update the window
    pygame.display.update()