import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game !!!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
Green = (0, 255, 0)

# Load explosion image
explosion_image = pygame.image.load(r"c:\Users\Rvkko's computer\Pictures\623cdcca882db2d7efa8d32424a61d29_w200.gif")
explosion_image = pygame.transform.scale(explosion_image, (50, 50))  # Resize to match the player size
player_hit_sound = pygame.mixer.Sound("c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-2-236688.mp3")
enemy_hit_sound = pygame.mixer.Sound("c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-1-236678.mp3")
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

# Load images
player_image = pygame.image.load("c:\\Users\\Rvkko's computer\\Pictures\\BAOyZX.png")  # Update with the actual path
enemy_image = pygame.image.load("c:\\Users\\Rvkko's computer\\Pictures\\mini1.png")  # Update with the actual path
player_image = pygame.transform.scale(player_image, (50, 50))  # Ensure the image is the correct size
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Ensure the image is the correct size

bullet_size = 5
bullets = []

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont("monospace", 35)

# Clock for FPS
clock = pygame.time.Clock()

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size]  # Center horizontally, aligned at the bottom
player_list = [player_pos]
player_list = 7

bullet_size = 5
bullets = []

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
enemy_speed = 7

# Score
score = 0
font = pygame.font.SysFont("monospace", 35)

# Clock for FPS
clock = pygame.time.Clock()

game_over = False

# Shooting mechanics
last_shot_time = 0  # Initialize last shot time
shot_cooldown = 2.0  # 2 seconds cooldown for shooting

# Friendly rocket ships
friendly_rocket_size = 30
friendly_rockets = []  # List to store friendly rockets
friendly_rocket_speed = 10  # Speed of friendly rockets

# Enemy rocket ships
enemy_rocket_size = 30
enemy_rockets = []  # List to store enemy rockets
enemy_rocket_speed = 5  # Speed of enemy rockets

def drop_enemies(enemy_list):
    if len(enemy_list) < 10:
        enemy_x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([enemy_x_pos, 0])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        # Replace the rectangle with the image
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

def update_enemy_positions(enemy_list):
    global score, game_over
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)

def draw_bullets(bullets):
    for bullet_pos in bullets:
        pygame.draw.rect(screen, WHITE, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

def update_bullet_positions(bullets):
    for idx, bullet_pos in enumerate(bullets):
        if bullet_pos[1] > 0:
            bullet_pos[1] -= 15
        else:
            bullets.pop(idx)

def check_collision(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if (enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size and
            enemy_pos[1] < player_pos[1] < enemy_pos[1] + enemy_size):
            return True
    return False

def check_bullet_collision(enemy_list, bullets):
    global score
    for enemy_pos in enemy_list[:]:  # Copy to avoid modifying the list while iterating
        for bullet_pos in bullets[:]:  # Copy to avoid modifying the list while iterating
            if (enemy_pos[0] < bullet_pos[0] < enemy_pos[0] + enemy_size and
                enemy_pos[1] < bullet_pos[1] < enemy_pos[1] + enemy_size):
                enemy_list.remove(enemy_pos)  # Remove enemy on collision
                bullets.remove(bullet_pos)  # Remove bullet on collision
                score += 1  # Increase score on hit
                break  # Exit inner loop

# New function to draw friendly rockets
def draw_friendly_rockets(friendly_rockets):
    for rocket_pos in friendly_rockets:
        pygame.draw.rect(screen, (0, 255, 0), (rocket_pos[0], rocket_pos[1], friendly_rocket_size, friendly_rocket_size))  # Green rockets

# New function to update friendly rockets
def update_friendly_rockets(friendly_rockets):
    for idx, rocket_pos in enumerate(friendly_rockets):
        if rocket_pos[1] > 0:
            rocket_pos[1] -= friendly_rocket_speed
        else:
            friendly_rockets.pop(idx)  # Remove rocket if it goes off-screen

# New function to draw enemy rockets
def draw_enemy_rockets(enemy_rockets):
    for rocket_pos in enemy_rockets:
        pygame.draw.rect(screen, (255, 0, 0), (rocket_pos[0], rocket_pos[1], enemy_rocket_size, enemy_rocket_size))  # Red rockets

# New function to update enemy rockets
def update_enemy_rockets(enemy_rockets):
    for idx, rocket_pos in enumerate(enemy_rockets):
        if rocket_pos[1] < HEIGHT:
            rocket_pos[1] += enemy_rocket_speed
        else:
            enemy_rockets.pop(idx)  # Remove rocket if it goes off-screen

# New function to check collision between friendly rockets and enemies
def check_friendly_collision(enemy_list, friendly_rockets):
    global score
    for enemy_pos in enemy_list[:]:  # Copy to avoid modifying the list while iterating
        for rocket_pos in friendly_rockets[:]:  # Copy to avoid modifying the list while iterating
            if (enemy_pos[0] < rocket_pos[0] < enemy_pos[0] + enemy_size and
                enemy_pos[1] < rocket_pos[1] < enemy_pos[1] + enemy_size):
                enemy_list.remove(enemy_pos)  # Remove enemy on collision
                friendly_rockets.remove(rocket_pos)  # Remove rocket on collision
                score += 1  # Increase score on hit
                break  # Exit inner loop

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Game over screen
    if game_over:
        screen.fill(BLACK)
        screen.blit(explosion_image, (player_pos[0], player_pos[1]))  # Show explosion at player position
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render("Final Score: " + str(score), True, WHITE)
        exit_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - 200, HEIGHT // 2 + 50))

        # Allow player to exit or restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:  # Quit the game
            pygame.quit()
            sys.exit()
        if keys[pygame.K_r]:  # Restart the game
            game_over = False
            player_pos = [WIDTH // 2, HEIGHT - player_size]  # Reset player position to the bottom
            bullets.clear()  # Clear bullets
            enemy_list.clear()  # Clear enemies
            score = 0  # Reset score

    if not game_over:
        keys = pygame.key.get_pressed()

        # Move the player left and right
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 10

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Shoot bullets
        if keys[pygame.K_SPACE] and current_time - last_shot_time >= shot_cooldown:  # Check if cooldown is complete
            if len(bullets) < 2:  # Allow up to two bullets
                bullets.append([player_pos[0] + player_size // 2, player_pos[1]])
                last_shot_time = current_time  # Update the last shot time

        screen.fill(BLACK)

        drop_enemies(enemy_list)
        update_enemy_positions(enemy_list)
        update_bullet_positions(bullets)

        # Check for collision between player and enemies
        if check_collision(enemy_list, player_pos):
            game_over = True  # Set game over flag if collision occurs

        # Check for collisions between bullets and enemies
        check_bullet_collision(enemy_list, bullets)

        draw_enemies(enemy_list)
        draw_bullets(bullets)
        screen.blit(player_image, (player_pos[0], player_pos[1]))  # Draw player image instead of rectangle

        # Display score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)
