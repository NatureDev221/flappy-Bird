import pygame, sys, random

pygame.init()

# === Window ===
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird - High Graphics")

# === Load Images ===
bg = pygame.image.load("images/background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

ground = pygame.image.load("images/ground.png").convert_alpha()
ground = pygame.transform.scale(ground, (WIDTH, 100))

bird_frames = [
    pygame.image.load("images/bird_wing_up.png").convert_alpha(),
    pygame.image.load("images/bird_wing_down.png").convert_alpha(),
    pygame.image.load("images/bird_wing_up.png").convert_alpha()
]

bird_index = 0
bird_img = bird_frames[bird_index]
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

pipe_body = pygame.image.load("images/pipe_body.png").convert_alpha()
pipe_end = pygame.image.load("images/pipe_end.png").convert_alpha()

# === Game Variables ===
gravity = 0.25
bird_movement = 0
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_gap = 160
pipe_speed = 3
score = 0
font = pygame.font.Font(None, 48)
game_active = True

# === Animation Timer for Bird ===
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# === Functions ===
def create_pipe():
    """Create top and bottom pipe pairs."""
    random_pos = random.randint(180, 420)
    bottom_pipe = build_pipe(random_pos)
    top_pipe = build_pipe(random_pos - pipe_gap, flipped=True)
    return bottom_pipe, top_pipe

def build_pipe(y, flipped=False):
    """Build a complete pipe (body + end)."""
    pipe_height = 400
    pipe_surface = pygame.Surface((70, pipe_height), pygame.SRCALPHA)
    for i in range(0, pipe_height, pipe_body.get_height()):
        pipe_surface.blit(pipe_body, (0, i))
    pipe_surface.blit(pipe_end, (0, 0))
    if flipped:
        pipe_surface = pygame.transform.flip(pipe_surface, False, True)
    rect = pipe_surface.get_rect(midtop=(WIDTH + 70, y)) if not flipped else pipe_surface.get_rect(midbottom=(WIDTH + 70, y))
    return [pipe_surface, rect]

def move_pipes(pipes):
    """Scroll pipes to the left."""
    new_list = []
    for surf, rect in pipes:
        rect.centerx -= pipe_speed
        if rect.right > 0:
            new_list.append((surf, rect))
    return new_list

def draw_pipes(pipes):
    """Draw pipe bodies and ends."""
    for surf, rect in pipes:
        screen.blit(surf, rect)

def check_collision(pipes):
    """Return False if collision occurs."""
    for surf, rect in pipes:
        if bird_rect.colliderect(rect):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT - 100:
        return False
    return True

def draw_base(x_pos):
    screen.blit(ground, (x_pos, HEIGHT - 100))
    screen.blit(ground, (x_pos + WIDTH, HEIGHT - 100))

def draw_score(score):
    text = font.render(str(int(score)), True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

def rotate_bird(bird):
    """Tilt the bird depending on speed."""
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

# === Base scrolling ===
base_x = 0

# === Game Loop ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(bird_frames)
            bird_img = bird_frames[bird_index]

    # === Background ===
    screen.blit(bg, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_frames[bird_index])
        screen.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

        # Score
        score += 0.01
        draw_score(score)
    else:
        game_over_text = font.render("SKILL ISSUE", True, (255, 50, 50))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
        restart_text = font.render("Press SPACE", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

    # === Ground ===
    base_x -= 1
    draw_base(base_x)
    if base_x <= -WIDTH:
        base_x = 0

    pygame.display.update()
    clock.tick(60)
