import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 120
PLAYER_SIZE = 50
BULLET_SIZE = 5
ENEMY_SIZE = 50
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

explosion_image = load_image(r"c:\Users\Rvkko's computer\Pictures\623cdcca882db2d7efa8d32424a61d29_w200.gif", (50, 50))
player_hit_sound = pygame.mixer.Sound("c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-2-236688.mp3")
enemy_hit_sound = pygame.mixer.Sound("c:\\Users\\Rvkko's computer\\Downloads\\retro-explode-1-236678.mp3")

player_image = load_image("c:\\Users\\Rvkko's computer\\Pictures\\BAOyZX.png", (PLAYER_SIZE, PLAYER_SIZE))
enemy_image = load_image("c:\\Users\\Rvkko's computer\\Pictures\\mini1.png", (PLAYER_SIZE, PLAYER_SIZE))
bullet_image = load_image("c:\\Users\Rvkko's computer\\Pictures\\66cb7c87c36bc8152d8f80b5.png", (15, 19))

# Game variables
bullets = []
enemy_list = []
score = 0
font = pygame.font.SysFont("monospace", 35)
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
                return item1, item2
    return None

# Game functions
def login_screen():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
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

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(BLACK)
        txt_surface = font.render(text, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

# Button function
def create_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = active_color if x + width > mouse[0] > x and y + height > mouse[1] > y else inactive_color
    pygame.draw.rect(screen, color, (x, y, width, height))

    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (x + (width // 2 - button_text.get_width() // 2), y + (height // 2 - button_text.get_height() // 2)))

    return click[0] == 1 and color == active_color

def main_game(player_name):
    global score, enemy_list, bullets
    game_over = False
    player_pos = [WIDTH // 2, HEIGHT - PLAYER_SIZE]
    last_shot_time = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        
        # Player name
        name_text = font.render(f"Player: {player_name}", True, WHITE)
        screen.blit(name_text, (WIDTH - name_text.get_width(), 10))

        # Show score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

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
            if keys[pygame.K_SPACE] and current_time - last_shot_time >= 2000 and len(bullets) < 2:
                bullets.append([player_pos[0] + PLAYER_SIZE // 2, player_pos[1]])
                last_shot_time = current_time

            drop_enemies(enemy_list)
            update_positions(enemy_list, 3)
            update_positions(bullets, 15, is_bullet=True)

            draw_entities(enemy_image, enemy_list)
            draw_entities(bullet_image, bullets)

            if check_collision(enemy_list, [player_pos], ENEMY_SIZE, PLAYER_SIZE):
                player_hit_sound.play()
                game_over = True

            if check_collision(bullets, enemy_list, BULLET_SIZE, ENEMY_SIZE):
                bullets.remove(bullets[0])
                enemy_list.remove(enemy_list[0])
                score += 1
                enemy_hit_sound.play()

        # Game over screen
        if game_over:
            screen.fill(BLACK)
            screen.blit(explosion_image, (player_pos[0], player_pos[1]))
            game_over_text = font.render("Game Over!", True, WHITE)
            score_text = font.render("Final Score: " + str(score), True, WHITE)
            exit_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
            
            # Calculate button_y for positioning
            button_y = HEIGHT // 2 + 50  # Y position of the "Restart" button

            # Get the rectangle for the game over text and position it above the buttons
            game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, button_y - 150))  # 100 pixels above the buttons
            score_text_rect = score_text.get_rect(center=(WIDTH // 2, button_y - 100))  # 50 pixels above the buttons
            exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, button_y - 50))  # Aligned with the buttons

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(exit_text, exit_text_rect)

            while game_over:
                pygame.display.update()

                if create_button("Restart Game", WIDTH // 2 - 100, HEIGHT // 2 + 50, 250, 50, (0, 128, 0), (0, 200, 0)):
                    game_over = False
                    enemy_list.clear()
                    bullets.clear()
                    score = 0
                    break

                if create_button("Change Name", WIDTH // 2 - 100, HEIGHT // 2 + 120, 250, 50, (128, 0, 0), (200, 0, 0)):
                    return "change_name"

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        player_name = login_screen()  # Initial login screen
        result = main_game(player_name)  # Play the game

        if result == "change_name":
            player_name = login_screen()  # Go back to login screen to change name