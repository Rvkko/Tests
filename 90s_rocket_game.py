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
high_score = 0  # Initialize high score
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

# score
score = 0
high_score = 0  # Initialize high score
font = pygame.font.SysFont("monospace", 35)

# Clock for FPS
clock = pygame.time.Clock()
player_name = ""  # Store player name
input_active = True  # Track if input is active

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

name_entry = True  # New variable to track name entry
player_name = ""  # Variable to store player's name

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
            game_over = True  # Trigger game over if an enemy reaches the bottom

def draw_bullets(bullets):
    for bullet_pos in bullets:
        screen.blit(bullet_image, (bullet_pos[0], bullet_pos[1]))  # Draw bullet image
        
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

# Function to input player's name and ensure the game doesn't start with a mouse click
def input_player_name():
    global player_name, input_active
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    font = pygame.font.Font(None, 32)
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keep the input box active when clicking inside it
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True  # No change to this behavior, just ensuring input remains active

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        return text  # Exit input when Enter is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

# Game loop
while True:
    if input_active:
        player_name = input_player_name()  # Prompt for player name
        input_active = False

    screen.fill(BLACK)
    draw_enemies(enemy_list)
    update_enemy_positions(enemy_list)
    draw_bullets(bullets)
    
    if game_over:
        screen.fill(BLACK)
        screen.blit(explosion_image, (player_pos[0], player_pos[1]))

        game_over_text = font.render("GAME OVER!")
        score_text = font("Final Score:" + str(score), True, WHITE)
        exit_text = font.render("Press R to Restart or Quit", True, WHITE)
        
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(exit_text, exit_text_rect)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:  # Quit the game
            name_entry = True  # Bring back to name entry screen
            game_over = False
            player_name = ""  # Reset player name
            score = 0  # Reset score

        if keys[pygame.K_r]:  # Restart the game
            game_over = False
            player_pos = [WIDTH // 2, HEIGHT - player_size]
            bullets.clear()
            enemy_list.clear()
            score = 0

    if not game_over:
        # Move player
        keys = pygame.key.get_pressed()  # Get the state of all keys
        if keys[pygame.K_a]:  # Move left
            player_pos[0] -= 5  # Move player left by 5 pixels
        if keys[pygame.K_d]:  # Move right
            player_pos[0] += 5  # Move player right by 5 pixels

        # Ensure the player doesn't move off-screen
        player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))  # Clamp position to screen boundaries

        # Shoot bullet on space bar
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - last_shot_time >= shot_cooldown:
                bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]]
                bullets.append(bullet_pos)
                last_shot_time = current_time

        # Drop enemies and update their positions
        drop_enemies(enemy_list)

        # Display score
        score_text = f"Score: {score}  High Score: {high_score}"  
        score_label = font.render(score_text, True, WHITE)
        screen.blit(score_label, (10, 10))

    # Update the screen and control frame rate
    pygame.display.update()
    clock.tick(30)  # Cap the frame rate

