import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змеюга 3")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_START = (112, 10, 171)
COLOR_END = (225, 180, 251)
def interpolate_color(start_color, end_color, factor):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor)
    )

food_sprites = [
    {"image": pygame.image.load("apple.png"), "chance": 0.6, "points": 1},
    {"image": pygame.image.load("banana.png"), "chance": 0.3, "points": 5},
    {"image": pygame.image.load("strawberry.png"), "chance": 0.1, "points": 10}
]

for food in food_sprites:
    food["image"] = pygame.transform.scale(food["image"], (CELL_SIZE, CELL_SIZE))

def get_random_food():
    rand = random.random()
    count = 0
    chance = food_sprites[count]["chance"]
    while rand > chance:
        count += 1
        chance += food_sprites[count]["chance"]
    return food_sprites[count]

snake = [(400, 400), (380, 400), (360, 400)]
len_for_speed = 3
direction = (CELL_SIZE, 0)

food = {"pos": (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)), "type": get_random_food()}
score = 0

font = pygame.font.Font(None, 30)

SNAKE_SPEED = 200
last_move_time = pygame.time.get_ticks()

last_key_time = pygame.time.get_ticks()
KEY_DELAY = SNAKE_SPEED

def draw_tail(tail_pos, tail_direction, color):
    x, y = tail_pos
    if tail_direction == (CELL_SIZE, 0):  # Вправо
        points = [(x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE // 2)]
    elif tail_direction == (-CELL_SIZE, 0):  # Влево
        points = [(x, y), (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE // 2)]
    elif tail_direction == (0, CELL_SIZE):  # Вниз
        points = [(x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), (x + CELL_SIZE // 2, y)]
    elif tail_direction == (0, -CELL_SIZE):  # Вверх
        points = [(x, y), (x + CELL_SIZE, y), (x + CELL_SIZE // 2, y + CELL_SIZE)]

    pygame.draw.polygon(screen, color, points)

def speed_game():
    global SNAKE_SPEED, len_for_speed, KEY_DELAY
    if len(snake) == len_for_speed + 5:
        len_for_speed += 5
        SNAKE_SPEED = int(SNAKE_SPEED * 0.9)
        KEY_DELAY = SNAKE_SPEED


# Функция отрисовки змейки с полукруглой головой и треугольным хвостом
def draw_snake():
    length = len(snake)

    for i, segment in enumerate(snake):
        color_factor = i / (length - 1) if length > 1 else 0
        segment_color = interpolate_color(COLOR_START, COLOR_END, color_factor)

        if i == 0:  # Голова змейки (полукруг)
            head_x, head_y = segment
            rect = pygame.Rect(head_x, head_y, CELL_SIZE, CELL_SIZE)

            if direction == (CELL_SIZE, 0):  # Движение вправо
                pygame.draw.circle(screen, segment_color, (head_x + CELL_SIZE//2, head_y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.rect(screen, segment_color, (head_x, head_y, CELL_SIZE//2, CELL_SIZE))
            elif direction == (-CELL_SIZE, 0):  # Движение влево
                pygame.draw.circle(screen, segment_color, (head_x + CELL_SIZE // 2, head_y + CELL_SIZE // 2), CELL_SIZE // 2)
                pygame.draw.rect(screen, segment_color, (head_x + CELL_SIZE // 2, head_y, CELL_SIZE // 2, CELL_SIZE))
            elif direction == (0, CELL_SIZE):  # Движение вниз
                pygame.draw.circle(screen, segment_color, (head_x + CELL_SIZE//2, head_y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.rect(screen, segment_color, (head_x, head_y, CELL_SIZE, CELL_SIZE//2))
            elif direction == (0, -CELL_SIZE):  # Движение вверх
                pygame.draw.circle(screen, segment_color, (head_x + CELL_SIZE//2, head_y + CELL_SIZE//2), CELL_SIZE//2)
                pygame.draw.rect(screen, segment_color, (head_x, head_y + CELL_SIZE//2, CELL_SIZE, CELL_SIZE//2))

        elif i == len(snake) - 1:  # Хвост змейки (треугольник)
            dx = (snake[-2][0] - snake[-1][0]) % WIDTH
            dy = (snake[-2][1] - snake[-1][1]) % HEIGHT

            if dx == CELL_SIZE and dy == 0:
                tail_direction = (CELL_SIZE, 0)
            elif dx == WIDTH - CELL_SIZE and dy == 0:
                tail_direction = (-CELL_SIZE, 0)
            elif dx == 0 and dy == CELL_SIZE:
                tail_direction = (0, CELL_SIZE)
            elif dx == 0 and dy == HEIGHT - CELL_SIZE:
                tail_direction = (0, -CELL_SIZE)
            else:
                print("Ошибка: tail_direction не определен", dx, dy)
                tail_direction = (CELL_SIZE, 0)

            draw_tail(segment, tail_direction, segment_color)

        else:  # Обычные сегменты тела
            pygame.draw.rect(screen, segment_color, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food():
    screen.blit(food["type"]["image"], food["pos"])

def show_score():
    text = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(text, (10, 10))

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background, (0, 0))

    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > SNAKE_SPEED:
        last_move_time = current_time

        new_head = (
            (snake[0][0] + direction[0]) % WIDTH,
            (snake[0][1] + direction[1]) % HEIGHT
        )

        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        if new_head == food["pos"]:
            score += food["type"]["points"]
            food = {"pos": (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)), "type": get_random_food()}
        else:
            snake.pop()


    current_key_time = pygame.time.get_ticks()
    if current_key_time - last_key_time > KEY_DELAY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                    last_key_time = current_key_time
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                    last_key_time = current_key_time
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                    last_key_time = current_key_time
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                    last_key_time = current_key_time

    draw_snake()
    draw_food()
    show_score()
    speed_game()

    pygame.display.flip()
    clock.tick(144)

pygame.quit()
