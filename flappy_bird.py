import pygame
import random

# Initialize pygame
pygame.init()

# Game window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game variables
gravity = 0.5
bird_movement = 0
score = 0
game_active = True

# Load assets
font = pygame.font.SysFont("Arial", 32)

# Bird
bird = pygame.Rect(100, HEIGHT // 2, 30, 30)

# Pipes
pipe_width = 60
pipe_gap = 150
pipe_list = []

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Game loop
clock = pygame.time.Clock()
while True:
    win.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -10
            if event.key == pygame.K_SPACE and not game_active:
                bird.center = (100, HEIGHT // 2)
                pipe_list.clear()
                bird_movement = 0
                score = 0
                game_active = True

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    if game_active:
        # Bird
        bird_movement += gravity
        bird.y += int(bird_movement)
        pygame.draw.ellipse(win, WHITE, bird)

        # Pipes
        for pipe in pipe_list:
            pipe.x -= 4
            pygame.draw.rect(win, GREEN, pipe)

        # Remove off-screen pipes
        pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]

        # Collision
        for pipe in pipe_list:
            if bird.colliderect(pipe):
                game_active = False

        if bird.top <= 0 or bird.bottom >= HEIGHT:
            game_active = False

        # Score
        for pipe in pipe_list:
            if pipe.centerx == bird.centerx:
                score += 1

        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

    else:
        msg = font.render("Game Over! Press SPACE to Restart", True, WHITE)
        win.blit(msg, (20, HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(60)