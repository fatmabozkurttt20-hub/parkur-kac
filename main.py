import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Parkur Kaç")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (15, 15, 20)
BLUE = (60, 140, 255)
RED = (230, 60, 60)
GREEN = (60, 220, 100)
GRAY = (90, 90, 100)
YELLOW = (255, 220, 60)

GROUND_Y = HEIGHT - 100

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

SAVE_FILE = os.path.expanduser("~/oyun/save.json")


def load_best():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f).get("best_score", 0)
        except Exception:
            return 0
    return 0


def save_best(value):
    with open(SAVE_FILE, "w") as f:
        json.dump({"best_score": value}, f)


best_score = load_best()

# Oyuncu
player_w, player_h = 40, 60
player_x = 80
player_y = GROUND_Y - player_h
player_vy = 0
gravity = 0.9
jump_force = -16
is_jumping = False
is_sliding = False
slide_h = 28

# Oyun durumu
game_speed = 6
score = 0
obstacles = []
spawn_timer = 0
spawn_interval = 70

game_over = False
game_started = False


def spawn_obstacle():
    kind = random.choice(["jump", "duck"])
    if kind == "jump":
        # Yerden yükselen engel - zıplayarak geçilir
        w, h = 30, 40
        y = GROUND_Y - h
    else:
        # Havada asılı engel - eğilerek geçilir
        w, h = 50, 30
        y = GROUND_Y - player_h - 10
    obstacles.append({"x": WIDTH + 50, "y": y, "w": w, "h": h, "kind": kind})


def reset_game():
    global player_y, player_vy, is_jumping, is_sliding, game_speed
    global score, obstacles, spawn_timer, spawn_interval, game_over, game_started
    player_y = GROUND_Y - player_h
    player_vy = 0
    is_jumping = False
    is_sliding = False
    game_speed = 6
    score = 0
    obstacles = []
    spawn_timer = 0
    spawn_interval = 70
    game_over = False
    game_started = True


def get_player_rect():
    h = slide_h if is_sliding else player_h
    y = player_y + (player_h - h) if is_sliding else player_y
    return pygame.Rect(player_x, y, player_w, h)


running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        press = event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN)
        release = event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP)

        if not game_started or game_over:
            if press:
                reset_game()
        else:
            if press:
                if not is_jumping:
                    player_vy = jump_force
                    is_jumping = True
                is_sliding = False
            # basılı tutma algısı için ayrı bir yaklaşım kullanıyoruz (aşağıda)

    if game_started and not game_over:
        # Basılı tutma durumunu kontrol et (eğilme)
        mouse_down = pygame.mouse.get_pressed()[0]
        touches_down = False
        if hasattr(pygame, "get_touches"):
            pass  # bazı sürümlerde yok, mouse yeterli test için
        is_sliding = mouse_down and not is_jumping

        # Yerçekimi ve zıplama
        player_vy += gravity
        player_y += player_vy
        if player_y >= GROUND_Y - player_h:
            player_y = GROUND_Y - player_h
            player_vy = 0
            is_jumping = False

        # Engel üretimi
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            spawn_obstacle()
            if spawn_interval > 40:
                spawn_interval -= 1

        # Engelleri hareket ettir
        for obs in obstacles[:]:
            obs["x"] -= game_speed
            if obs["x"] + obs["w"] < 0:
                obstacles.remove(obs)
                score += 1

        # Hız zamanla artar
        game_speed += 0.002

        # Çarpışma kontrolü
        player_rect = get_player_rect()
        for obs in obstacles:
            obs_rect = pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"])
            if player_rect.colliderect(obs_rect):
                game_over = True
                if score > best_score:
                    best_score = score
                    save_best(best_score)

    # ÇİZİM
    screen.fill(BLACK)

    # Zemin
    pygame.draw.rect(screen, GRAY, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    if not game_started:
        title = big_font.render("PARKUR KAÇ", True, BLUE)
        info = font.render("Başlamak için dokun", True, WHITE)
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 30))

    elif game_over:
        over_text = big_font.render("DÜŞTÜN!", True, RED)
        score_text = font.render(f"Skor: {score}", True, WHITE)
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        restart_text = font.render("Tekrar denemek için dokun", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

    else:
        # Engeller
        for obs in obstacles:
            color = RED if obs["kind"] == "jump" else (255, 140, 60)
            pygame.draw.rect(screen, color, (obs["x"], obs["y"], obs["w"], obs["h"]))

        # Oyuncu
        pr = get_player_rect()
        pygame.draw.rect(screen, BLUE, pr)

        # Skor
        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        best_text = font.render(f"En iyi: {best_score}", True, YELLOW)
        screen.blit(best_text, (10, 45))

    pygame.display.flip()

pygame.quit()
