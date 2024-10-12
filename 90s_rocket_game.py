import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 120
PLAYER_SIZE = 100
BULLET_SIZE = 20
ENEMY_SIZE = 100
FRIENDLY_ROCKET_SIZE = 30
ENEMY_ROCKET_SIZE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game !!!")

# images and sounds
def load_image(path, size=None):
    image = pygame.image.load(path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

explosion_image = load_image(r"c:/Users/Rvkko's computer/Pictures/623cdcca882db2d7efa8d32424a61d29_w200.gif", (50, 50))
player_hit_sound = pygame.mixer.Sound(r"c:/Users/Rvkko's computer/Downloads/retro-explode-2-236688.mp3")
enemy_hit_sound = pygame.mixer.Sound(r"c:/Users/Rvkko's computer/Downloads/retro-explode-1-236678.mp3")
space_background = pygame.image.load(r"c:/Users/Rvkko's computer/Downloads/space-1164579_1920.png")
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))
player_image = load_image(r"c:/Users/Rvkko's computer/Pictures/BAOyZX.png", (PLAYER_SIZE, PLAYER_SIZE))
enemy_image = load_image(r"c:/Users/Rvkko's computer/Pictures/mini1.png", (PLAYER_SIZE, PLAYER_SIZE))
bullet_image = load_image(r"c:/Users/Rvkko's computer/Pictures/66cb7c87c36bc8152d8f80b5.png", (20, 20))

# background music
pygame.mixer.music.load(r"c:/Users/Rvkko's computer/Downloads/Megaman 3 Theme.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

bullets = []
enemy_list = []
score = 0
leaderboard = []
font = pygame.font.SysFont("monospace", 35)
retro_font = pygame.font.Font(r"c:\\Users\\Rvkko's computer\\Downloads\\CsDegitaRegularDemo-lxVGe.otf", 50)
clock = pygame.time.Clock()

class Player:
    def __init__(self, name):
        self.name = name
        self.high_score = 0

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score

    def reset_high_score(self):
        self.high_score = 0

current_player = None

# display scores
def display_scores(current_score, high_score):
    current_score_text = font.render(f"Current Score: {current_score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    
    screen.blit(current_score_text, (50, 50))
    screen.blit(high_score_text, (50, 100))
    pygame.display.flip()

# enemy drop
def drop_enemies(enemy_list):
    if len(enemy_list) < 10:
        enemy_x_pos = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_list.append([enemy_x_pos, 0])

# player death
def player_death():
    global score, current_player
    current_player.update_high_score(score)
    pygame.mixer.music.stop()

# Draw entities
def draw_entities(image, positions):
    for pos in positions:
        screen.blit(image, (pos[0], pos[1]))

# Update positions
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

# Function to check collision
def check_collision(list1, list2, size1, size2):
    for item1 in list1:
        for item2 in list2:
            if (item1[0] < item2[0] + size2 and
                item1[0] + size1 > item2[0] and
                item1[1] < item2[1] + size2 and
                item1[1] + size1 > item2[1]):
                player_death()
                return list1.index(item1), list2.index(item2)
    return None

# Ensure all buttons in the code use the updated create_button function
def login_screen():
    global current_player, score
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
                        current_player = Player(text)
                        score = 0
                        return
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

# Show leaderboard
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

# Main game loop
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
    power_up_bar = 0
    kills = 0
    rapid_fire_active = False
    rapid_fire_start_time = 0
    bullet_count = 1  # Start with 1 bullet

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # space background
        screen.blit(space_background, (0, 0))

        # Player name
        name_text = font.render(f"Player: {player_name}", True, WHITE)
        screen.blit(name_text, (WIDTH - name_text.get_width(), 10))

        # Show score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # high score
        high_score_text = font.render(f"High Score: {current_player.high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 50))

        # Check for power-up
        if score > 0 and score % 10 == 0 and not power_up_active:
            power_up_active = True
            player_health = 2
            power_up_bar = 100

        # Update power-up
        if power_up_active:
            power_up_bar -= 0.08
            if power_up_bar <= 0:
                power_up_active = False
                player_health = 1
                power_up_bar = 0
                
            # power-up bar
            pygame.draw.rect(screen, (255, 215, 0), (10, 90, power_up_bar, 20))  # Gold color

        if not game_over:
            # Move player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_pos[0] > 0:
                player_pos[0] -= 5
            if keys[pygame.K_d] and player_pos[0] < WIDTH - PLAYER_SIZE:
                player_pos[0] += 5

            # Shooting
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - last_shot_time >= (100 if rapid_fire_active else 500):
                if len(bullets) < 4:  # Allow up to 4 bullets (2 shots of 2 bullets each)
                    for _ in range(bullet_count):
                        bullets.append([player_pos[0] + PLAYER_SIZE // 2 - 10, player_pos[1]])
                    last_shot_time = current_time

            drop_enemies(enemy_list)
            update_positions(enemy_list, 3)
            update_positions(bullets, 15, is_bullet=True)

            # Check for collisions
            bullets_to_remove = []
            enemies_to_remove = []
            for bullet in bullets:
                for enemy in enemy_list:
                    if (bullet[0] < enemy[0] + ENEMY_SIZE and
                        bullet[0] + BULLET_SIZE > enemy[0] and
                        bullet[1] < enemy[1] + ENEMY_SIZE and
                        bullet[1] + BULLET_SIZE > enemy[1]):
                        bullets_to_remove.append(bullet)
                        enemies_to_remove.append(enemy)
                        score += 1
                        current_player.update_high_score(score)

            # Remove bullets and enemies
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)
            for enemy in enemies_to_remove:
                if enemy in enemy_list:
                    enemy_list.remove(enemy)

            # Draw entities
            draw_entities(player_image, [player_pos])
            draw_entities(enemy_image, enemy_list)
            draw_entities(bullet_image, bullets)

        pygame.display.flip()
        clock.tick(FPS)

            # power-up bar
        pygame.draw.rect(screen, (255, 215, 0), (10, 90, power_up_bar, 20))  # Gold color

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
            if keys[pygame.K_SPACE] and current_time - last_shot_time >= (100 if rapid_fire_active else 500):
                if len(bullets) < 4:  # Allow up to 4 bullets (2 shots of 2 bullets each)
                    for _ in range(bullet_count):
                        bullets.append([player_pos[0] + PLAYER_SIZE // 2 - 10, player_pos[1]])
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
                power_up_active = False
                del enemy_list[collision[0]]
            else:
                player_hit_sound.play()
                game_over = True

        if check_collision(bullets, enemy_list, BULLET_SIZE, ENEMY_SIZE):
            bullet_idx, enemy_idx = check_collision(bullets, enemy_list, BULLET_SIZE, ENEMY_SIZE)
            del bullets[bullet_idx]
            del enemy_list[enemy_idx]
            score += 1
            kills += 1
            enemy_hit_sound.play()

        if kills >= 20 and not rapid_fire_active:
            rapid_fire_active = True
            rapid_fire_start_time = pygame.time.get_ticks()

        # Increase 0.5% power-up when active
        if power_up_active:
            power_up_bar = min(100, power_up_bar + 0.5)

        # Increase bullet count after 10 hits
        if score == 10:
            bullet_count = 2

        # Check if rapid-fire deactivated
        if rapid_fire_active and pygame.time.get_ticks() - rapid_fire_start_time >= 10000:
            rapid_fire_active = False
            kills = 0

        # Game over screen
        if game_over:
            if score > current_player.high_score:
                current_player.high_score = score

            leaderboard.append({"name": player_name, "score": score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]

            screen.blit(space_background, (0, 0))  # Use the same background for game over screen
            screen.blit(explosion_image, (player_pos[0], player_pos[1]))
            game_over_text = retro_font.render("Game Over!", True, WHITE)
            score_text = retro_font.render(f"Final Score: {score}", True, WHITE)
            high_score_txt = retro_font.render(f"High Score: {current_player.high_score}", True, WHITE)
            exit_text = retro_font.render("Press ESC to Quit", True, WHITE)
            
            center_x = WIDTH // 2 + 50
            game_over_text_rect = game_over_text.get_rect(center=(center_x - 20, HEIGHT // 2 - 100))
            score_text_rect = score_text.get_rect(center=(center_x, HEIGHT // 2 - 50))
            high_score_text_rect = high_score_txt.get_rect(center=(center_x, HEIGHT // 2))
            exit_text_rect = exit_text.get_rect(center=(center_x, HEIGHT // 2 + 50))

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(high_score_txt, high_score_text_rect)
            screen.blit(exit_text, exit_text_rect)

            while game_over:
                pygame.display.update()

                if create_button("Restart Game", WIDTH // 2 - 125, HEIGHT // 2 + 100, (0, 128, 0), (0, 200, 0)):
                    game_over = False
                    enemy_list.clear()
                    bullets.clear()
                    score = 0
                    bullet_count = 1  # Reset bullet count on restart
                    break

                if create_button("Change Name", WIDTH // 2 - 125, HEIGHT // 2 + 170, (128, 0, 0), (200, 0, 0)):
                    high_score = 0  # Reset high score when changing name
                    return "change_name"

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)

        if power_up_active:
            power_up_bar = min(100, power_up_bar + 50)

if __name__ == "__main__":
    player_name = login_screen()
    while True:
        result = main_game(player_name)
        
        if result == "change_name":
            player_name = login_screen()
        else:
            break
