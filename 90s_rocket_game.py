import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 120
PLAYER_SIZE = 100
BULLET_SIZE = 20  # Adjusted to match bullet image size
ENEMY_SIZE = 100
FRIENDLY_ROCKET_SIZE = 30
ENEMY_ROCKET_SIZE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game !!!")

# Load images and sounds
def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

explosion_image = load_image(r"c:\\Users\\Rvkko's computer\\Pictures\\623cdcca882db2d7efa8d32424a61d29_w200.gif", (50, 50))
player_hit_sound = pygame.mixer.Sound(r"c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-2-236688.mp3")
enemy_hit_sound = pygame.mixer.Sound(r"c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-1-236678.mp3")
space_background = pygame.image.load(r"c:\Users\Rvkko's computer\Downloads\space-1164579_1920.png")
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))
player_image = load_image(r"c:\\Users\\Rvkko's computer\\Pictures\\BAOyZX.png", (PLAYER_SIZE, PLAYER_SIZE))
enemy_image = load_image(r"c:\\Users\\Rvkko's computer\\Pictures\\mini1.png", (PLAYER_SIZE, PLAYER_SIZE))
bullet_image = load_image(r"c:\\Users\\Rvkko's computer\\Pictures\\66cb7c87c36bc8152d8f80b5.png", (20, 20))

# Game variables
bullets = []
enemy_list = []
score = 0
high_score = 0  # Initialize high score
leaderboard = []  # Initialize leaderboard
font = pygame.font.SysFont("monospace", 35)
retro_font = pygame.font.Font(r"c:\\Users\\Rvkko's computer\\Downloads\\CsDegitaRegularDemo-lxVGe.otf", 50)
clock = pygame.time.Clock()

def drop_enemies(enemy_list):
    if len(enemy_list) < 10:
        enemy_x_pos = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_list.append([enemy_x_pos, 0])

def draw_entities(image, positions):
    for pos in positions:
        screen.blit(image, (pos[0], pos[1]))

def update_positions(positions, speed, is_bullet=False):
    for idx, pos in enumerate(positions):
        if is_bullet:
            if pos[1] > 0:
                pos[1] -= 15
            else:
                positions.pop(idx)
        else:
            if pos[1] < HEIGHT:
                pos[1] += speed
            else:
                positions.pop(idx)

def check_collision(list1, list2, size1, size2):
    for item1 in list1:
        for item2 in list2:
            if (item1[0] < item2[0] + size2 and
                item1[0] + size1 > item2[0] and
                item1[1] < item2[1] + size2 and
                item1[1] + size1 > item2[1]):
                return list1.index(item1), list2.index(item2)
    return None

def login_screen():
    # Define retro colors for text and input box
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('cyan')
    background_color = (20, 20, 30)  # Dark background
    neon_purple = pygame.Color('purple')
    
    # Use default font for title text
    title_font = pygame.font.SysFont("monospace", 50)
    input_font = pygame.font.Font(r"c:\\Users\\Rvkko's computer\\Downloads\\CsDegitaRegularDemo-lxVGe.otf", 35)
    
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)  # Wider text box for retro look
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(background_color)
        title_text = title_font.render("Enter Player Name", True, neon_purple)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

        # Display input text in retro font
        txt_surface = input_font.render(text, True, color_active)
        input_box.w = max(300, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        
        # Draw the input box with retro neon effect
        pygame.draw.rect(screen, color, input_box, 4)

        # Center the leaderboard button with the input box
        button_width = 250
        button_height = 50
        button_x = input_box.centerx - button_width // 2
        button_y = input_box.y + input_box.height + 20  # Add some space below the input box

        if create_button("Leaderboard", button_x, button_y, (0, 128, 0), (0, 200, 0)):
            show_leaderboard()

        pygame.display.flip()
        clock.tick(30)

def show_leaderboard():
    background_color = (20, 20, 30)  # Dark background
    screen.fill(background_color)
    title_font = pygame.font.SysFont("monospace", 50)
    leaderboard_font = pygame.font.SysFont("monospace", 35)
    title_text = title_font.render("Leaderboard", True, pygame.Color('cyan'))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Display leaderboard entries
    for idx, entry in enumerate(leaderboard):
        entry_text = leaderboard_font.render(f"{idx + 1}. {entry['name']} - {entry['score']}", True, pygame.Color('white'))
        screen.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, 150 + idx * 40))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

# Button function with retro styling and dynamic sizing
def create_button(text, x, y, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Use retro font for button text
    button_text = retro_font.render(text, True, WHITE)
    width = button_text.get_width() + 20  # Add padding
    height = button_text.get_height() + 10  # Add padding
    
    color = active_color if x + width > mouse[0] > x and y + height > mouse[1] > y else inactive_color
    pygame.draw.rect(screen, color, (x, y, width, height))
    screen.blit(button_text, (x + 10, y + 5))  # Center text within the button

    return click[0] == 1 and color == active_color

# Ensure all buttons in the code use the updated create_button function
def login_screen():
    # Define retro colors for text and input box
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('cyan')
    background_color = (20, 20, 30)  # Dark background
    neon_purple = pygame.Color('purple')
    
    # Use default font for title text
    title_font = pygame.font.SysFont("monospace", 50)
    input_font = pygame.font.Font(r"c:\\Users\\Rvkko's computer\\Downloads\\CsDegitaRegularDemo-lxVGe.otf", 35)
    
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)  # Wider text box for retro look
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(background_color)
        title_text = title_font.render("Enter Player Name", True, neon_purple)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

        # Display input text in retro font
        txt_surface = input_font.render(text, True, color_active)
        input_box.w = max(300, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        
        # Draw the input box with retro neon effect
        pygame.draw.rect(screen, color, input_box, 4)

        # Create leaderboard button
        if create_button("Leaderboard", WIDTH // 2 - 125, HEIGHT // 2 + 100, (0, 128, 0), (0, 200, 0)):
            show_leaderboard()

        pygame.display.flip()
        clock.tick(30)

def show_leaderboard():
    background_color = (20, 20, 30)  # Dark background
    screen.fill(background_color)
    title_font = pygame.font.SysFont("monospace", 50)
    leaderboard_font = pygame.font.SysFont("monospace", 35)
    title_text = title_font.render("Leaderboard", True, pygame.Color('cyan'))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Display leaderboard entries
    for idx, entry in enumerate(leaderboard):
        entry_text = leaderboard_font.render(f"{idx + 1}. {entry['name']} - {entry['score']}", True, pygame.Color('white'))
        screen.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, 150 + idx * 40))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

def main_game(player_name):
    global score, high_score, enemy_list, bullets, leaderboard
    score = 0
    game_over = False
    player_pos = [WIDTH // 2, HEIGHT - PLAYER_SIZE]
    bullets = []
    enemy_list = []
    last_shot_time = 0
    power_up_active = False
    player_health = 1
    power_up_bar = 0  # Initialize power-up bar
    kills = 0  # Track the number of kills
    rapid_fire_active = False  # Track rapid-fire status
    rapid_fire_start_time = 0  # Track rapid-fire start time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the space background
        screen.blit(space_background, (0, 0))

        # Player name
        name_text = font.render(f"Player: {player_name}", True, WHITE)
        screen.blit(name_text, (WIDTH - name_text.get_width(), 10))

        # Show score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Show high score
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 50))

        # Check for power-up activation
        if score > 0 and score % 10 == 0 and not power_up_active:
            power_up_active = True
            player_health = 2  # Player can get hit once without dying
            power_up_bar = 100  # Set power-up bar to 100%

        # Update power-up status
        if power_up_active:
            # Decrease power-up bar over time
            power_up_bar -= 0.05  # Slower decrement rate
            if power_up_bar <= 0:
                power_up_active = False
                player_health = 1  # Reset player health
                power_up_bar = 0  # Ensure the bar doesn't go below 0

            # Draw power-up bar
            pygame.draw.rect(screen, (255, 215, 0), (10, 90, power_up_bar, 20))  # Gold color

            # Draw thunder effect
            for i in range(int(power_up_bar // 10)):  # Adjust the number of thunder images
                screen.blit(thunder_image, (10 + i * 20, 90))

        if not game_over:
            screen.blit(player_image, (player_pos[0], player_pos[1]))

            # Move player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_pos[0] > 0:
                player_pos[0] -= 5
            if keys[pygame.K_d] and player_pos[0] < WIDTH - PLAYER_SIZE:
                player_pos[0] += 5

            # Shooting
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - last_shot_time >= (100 if rapid_fire_active else 500):  # 100ms for rapid-fire
                if len(bullets) < 4:  # Allow up to 4 bullets (2 shots of 2 bullets each)
                    bullets.append([player_pos[0] + PLAYER_SIZE // 2 - 10, player_pos[1]])  # Left bullet
                    bullets.append([player_pos[0] + PLAYER_SIZE // 2 + 10, player_pos[1]])  # Right bullet
                    last_shot_time = current_time

            drop_enemies(enemy_list)
            update_positions(enemy_list, 3)
            update_positions(bullets, 15, is_bullet=True)

            draw_entities(enemy_image, enemy_list)
            draw_entities(bullet_image, bullets)

        collision = check_collision(enemy_list, [player_pos], ENEMY_SIZE, PLAYER_SIZE)
        if collision:
            if player_health > 1:
                player_health -= 1
                power_up_active = False  # Deactivate power-up
                del enemy_list[collision[0]]  # Remove the enemy that hit the player
            else:
                player_hit_sound.play()
                game_over = True

        if check_collision(bullets, enemy_list, BULLET_SIZE, ENEMY_SIZE):
            bullet_idx, enemy_idx = check_collision(bullets, enemy_list, BULLET_SIZE, ENEMY_SIZE)
            del bullets[bullet_idx]
            del enemy_list[enemy_idx]
            score += 1
            kills += 1  # Increment kills
            enemy_hit_sound.play()

            # Activate rapid-fire mode after 25 kills
            if kills >= 25 and not rapid_fire_active:
                rapid_fire_active = True
                rapid_fire_start_time = pygame.time.get_ticks()

            # Increase power-up bar by 0.5% if power-up is active
            if power_up_active:
                power_up_bar = min(100, power_up_bar + 0.5)

        # Check if rapid-fire mode should be deactivated
        if rapid_fire_active and pygame.time.get_ticks() - rapid_fire_start_time >= 10000:  # 10 seconds
            rapid_fire_active = False
            kills = 0  # Reset kills

        # Game over screen
        if game_over:
            # Update high score
            if score > high_score:
                high_score = score

            # Update leaderboard
            leaderboard.append({"name": player_name, "score": score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10 scores

            screen.fill(BLACK)
            screen.blit(explosion_image, (player_pos[0], player_pos[1]))
            game_over_text = retro_font.render("Game Over!", True, WHITE)
            score_text = retro_font.render("Final Score: " + str(score), True, WHITE)
            high_score_text = retro_font.render("High Score: " + str(high_score), True, WHITE)
            exit_text = retro_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            
            # Center the game over elements
            center_x = WIDTH // 1.8900
            game_over_text_rect = game_over_text.get_rect(center=(center_x, HEIGHT // 2 - 100))
            score_text_rect = score_text.get_rect(center=(center_x, HEIGHT // 2 - 50))
            high_score_text_rect = high_score_text.get_rect(center=(center_x, HEIGHT // 2))
            exit_text_rect = exit_text.get_rect(center=(center_x, HEIGHT // 2 + 50))

            # Adjust the x-coordinates to align based on the maximum width
            max_width = game_over_text.get_width()
            game_over_text_rect.x = center_x - max_width // 2
            score_text_rect.x = center_x - score_text.get_width() // 2
            high_score_text_rect.x = center_x - max_width // 2
            exit_text_rect.x = center_x - exit_text.get_width() // 2

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(high_score_text, high_score_text_rect)
            screen.blit(exit_text, exit_text_rect)

            while game_over:
                pygame.display.update()

                if create_button("Restart Game", WIDTH // 2 - 125, HEIGHT // 2 + 100, (0, 128, 0), (0, 200, 0)):
                    game_over = False
                    enemy_list.clear()
                    bullets.clear()
                    score = 0
                    break

                if create_button("Change Name", WIDTH // 2 - 125, HEIGHT // 2 + 170, (128, 0, 0), (200, 0, 0)):
                    return "change_name"

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)

            # Increase power-up bar by 0.5% if power-up is active
        if power_up_active:
            power_up_bar = min(100, power_up_bar + 50)

if __name__ == "__main__":
    player_name = login_screen()  # Initial name input
    while True:
        result = main_game(player_name)  # Run the game
        
        if result == "change_name":
            player_name = login_screen()  # Allow name change only once
        else:
            break  # Exit the loop after game over