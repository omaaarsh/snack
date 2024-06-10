import pygame
import random
from const import *

# initialize pygame library
pygame.init()

# make screen with Title
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# make a clock
CLOCK = pygame.time.Clock()

# make snake shape in the middle of the screen
INITIAL_X = WIDTH // 2
INITIAL_Y = HEIGHT // 2
SNAKE = [
    (INITIAL_X, INITIAL_Y),  # the head of the snake
    (INITIAL_X - BLOCKSIZE, INITIAL_Y),  # the body of the snake
    (INITIAL_X - 2 * BLOCKSIZE, INITIAL_Y)  # the tail of the snake
]

def DrawFood(SNAKE):
    while True:
        food_X = random.randint(0, (WIDTH - BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        food_Y = random.randint(0, (HEIGHT - BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        if (food_X, food_Y) not in SNAKE:
            break
    return food_X, food_Y

# initialize variables
DIRACTION = "RIGHT"
eat = False
foodX, foodY = DrawFood(SNAKE)

# gameloop
while RUNNING:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            # determine the direction
            if event.key == pygame.K_UP and DIRACTION != "DOWN":
                DIRACTION = "UP"
            elif event.key == pygame.K_DOWN and DIRACTION != "UP":
                DIRACTION = "DOWN"
            elif event.key == pygame.K_RIGHT and DIRACTION != "LEFT":
                DIRACTION = "RIGHT"
            elif event.key == pygame.K_LEFT and DIRACTION != "RIGHT":
                DIRACTION = "LEFT"

    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill(BACKGROUND)
    HEAD = SNAKE[0]

    # calculate the new head position
    if DIRACTION == "UP":
        new_head = (HEAD[0], HEAD[1] - BLOCKSIZE)
    elif DIRACTION == "DOWN":
        new_head = (HEAD[0], HEAD[1] + BLOCKSIZE)
    elif DIRACTION == "LEFT":
        new_head = (HEAD[0] - BLOCKSIZE, HEAD[1])
    elif DIRACTION == "RIGHT":
        new_head = (HEAD[0] + BLOCKSIZE, HEAD[1])

    # check if snake eats himself
    if new_head in SNAKE:
        GAMEOVER=True
    # check if snake touches the walls
    elif new_head[0]>=640 or new_head[0]<0 or new_head[1]>=480 or new_head[1]<0:
        GAMEOVER=True
    # add the new head at the front
    else:
        SNAKE.insert(0, new_head)
    # check if snake eats food
    if (foodX, foodY) == HEAD:
        eat = True
        foodX, foodY = DrawFood(SNAKE)
        SCORE+=1
        SPEED+=1
    else:
        # delete the tail if not eaten food
        if not eat:
            SNAKE.pop()
        else:
            eat = False

    # Draw food
    pygame.draw.rect(SCREEN, RED, [foodX, foodY, BLOCKSIZE, BLOCKSIZE])

    # Draw the snake
    for x, y in SNAKE:
        pygame.draw.rect(SCREEN, GREEN, [x, y, BLOCKSIZE, BLOCKSIZE])

    # Display score 
    font=pygame.font.Font(None,25)
    text=font.render(f"Score:{SCORE}",True,WHITE)
    SCREEN.blit(text,(10,10))
    if GAMEOVER:
        text=font.render(f"Game over ya 3sal",True,RED)
        SCREEN.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    # to update the screen
    pygame.display.flip()

    # to control speed of the snake
    CLOCK.tick(SPEED)

pygame.quit()
