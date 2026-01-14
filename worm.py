# import the libraries we need
import pygame          # game stuff (graphics, keyboard, window)
import random          # random numbers (for apple spawn)
import sys             # lets us close the program properly

# start pygame
pygame.init()

# game speed (frames per second)
FPS = 15
clock = pygame.time.Clock()  # controls how fast the game runs

# window size
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20               # size of each grid square

# create the game window
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Beginner Wormy")

# font for score + game over text
font = pygame.font.Font(None, 30)

# colours (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
GRAY = (40, 40, 40)

# direction values (just strings, easy to read)
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

# starting direction
direction = RIGHT

# how many cells fit in the window
CELLWIDTH = WINDOWWIDTH // CELLSIZE
CELLHEIGHT = WINDOWHEIGHT // CELLSIZE

# random starting position for the snake
start_x = random.randint(5, CELLWIDTH - 6)
start_y = random.randint(5, CELLHEIGHT - 6)

# snake body (list of blocks)
worm = [
    {"x": start_x, "y": start_y},         # head
    {"x": start_x - 1, "y": start_y},     # body
    {"x": start_x - 2, "y": start_y}      # tail
]

# random apple position
apple = {
    "x": random.randint(0, CELLWIDTH - 1),
    "y": random.randint(0, CELLHEIGHT - 1)
}

score = 0           # keeps track of score
game_over = False   # stops movement when you lose

# main game loop (runs forever)
while True:

    # check for events (keyboard, closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   # close pygame
            sys.exit()      # exit program

        # check key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT
            elif event.key == pygame.K_UP and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                direction = DOWN

    # only move if game isn't over
    if not game_over:

        head = worm[0]  # current head of the snake

        # figure out where the new head goes
        if direction == UP:
            new_head = {"x": head["x"], "y": head["y"] - 1}
        elif direction == DOWN:
            new_head = {"x": head["x"], "y": head["y"] + 1}
        elif direction == LEFT:
            new_head = {"x": head["x"] - 1, "y": head["y"]}
        elif direction == RIGHT:
            new_head = {"x": head["x"] + 1, "y": head["y"]}

        # add new head to the front of the snake
        worm.insert(0, new_head)

        # check if snake hits wall
        if (
            new_head["x"] < 0 or
            new_head["x"] >= CELLWIDTH or
            new_head["y"] < 0 or
            new_head["y"] >= CELLHEIGHT
        ):
            game_over = True

        # check if snake hits itself
        for segment in worm[1:]:
            if segment == new_head:
                game_over = True

        # check if snake eats apple
        if new_head == apple:
            score += 1  # increase score
            apple = {   # spawn new apple
                "x": random.randint(0, CELLWIDTH - 1),
                "y": random.randint(0, CELLHEIGHT - 1)
            }
        else:
            worm.pop()  # remove tail if no apple eaten

    # clear screen every frame
    screen.fill(BLACK)

    # draw grid lines
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOWWIDTH, y))

    # draw apple
    pygame.draw.rect(
        screen,
        RED,
        (apple["x"] * CELLSIZE, apple["y"] * CELLSIZE, CELLSIZE, CELLSIZE)
    )

    # draw snake
    for segment in worm:
        pygame.draw.rect(
            screen,
            DARKGREEN,
            (segment["x"] * CELLSIZE, segment["y"] * CELLSIZE, CELLSIZE, CELLSIZE)
        )

    # draw score text
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # show game over text
    if game_over:
        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, (WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2))

    # update the screen
    pygame.display.update()

    # control game speed
    clock.tick(FPS)
