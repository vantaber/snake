import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змеюга 3")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


snake = [(400, 400), (380, 400), (360, 400)]
direction = (CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
score = 0

font = pygame.font.Font(None, 30)

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def show_score():
    text = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(text, (10, 10))

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False

    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        score += 1
    else:
        snake.pop()

    draw_snake()
    draw_food()
    show_score()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
