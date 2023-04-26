import pygame
import math
from board import *

pygame.init()


lvls = "lvl1"
level = {"lvl1": (board1, 'blue', 15, 26), "lvl2": (board2, 'green', 15, 7)}
board = level[lvls][0]
color = level[lvls][1]
X, Y = level[lvls][2], level[lvls][3]
WIDTH = 600
HEIGHT = 720
b_y_size = len(board) - 1
b_x_size = len(board[0])
print(b_x_size, b_y_size)
#num1, num2 = 20, 20
num1 = ((HEIGHT - 40) // b_y_size)  # y
num2 = WIDTH // b_x_size # x
print(num1, num2)

no_frame = pygame.NOFRAME
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

PI = math.pi
player_images = []

for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'player_images/{i}.png'), (22, 22)))
player_x = num2 * X                          #WIDTH//2 - num2 // 2
player_y = num1 * Y
direction = 0
counter = 0
flicker = False

# L, R, U, D
Left, Right, Up, Down = False, False, False, False
turns_allowed = [Left, Right, Up, Down]
direction_command = 0
RIGHT, LEFT, UP, DOWN = 0, 1, 2, 3
player_speed = 1
ghost_speed = 2

scores = 0

def draw_board():
    board_x = (WIDTH - (num2 * b_x_size)) / 2
    # print(num1)
    line_thick, sdot, ldot = 3, 2, 6

    for i in range(len(board)):  # row
        for j in range(len(board[i])):  # column
            x, y = board_x + j * num2, i * num1
            mid_linex = x + num2 // 2 - (line_thick * 0.5) + 0.5
            mid_liney = y + num1 // 2 - (line_thick * 0.5) + 0.5
            #pygame.draw.rect(screen, 'yellow', (x, y, num2, num1), 1)
            if board[i][j] == 1:
                pygame.draw.circle(screen, 'white', (x + (0.5 * num2), y + (0.5 * num1)), sdot)
            if board[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'red', (x + (0.5 * num2), y + (0.5 * num1)), ldot)
            if board[i][j] == 3:  # VERTICAL
                pygame.draw.line(screen, color, (mid_linex, y), (mid_linex, y + num1), line_thick)
            if board[i][j] == 4:
                pygame.draw.line(screen, color, (x, mid_liney), (x + num2, mid_liney), line_thick)
            if board[i][j] == 5:
                pygame.draw.line(screen, color, (x, mid_liney), (mid_linex, mid_liney), line_thick)
                pygame.draw.line(screen, color, (mid_linex, mid_liney), (mid_linex, y + num1), line_thick)
            if board[i][j] == 6:
                pygame.draw.line(screen, color, (mid_linex, mid_liney), (x + num2, mid_liney), line_thick)
                pygame.draw.line(screen, color, (mid_linex, mid_liney), (mid_linex, y + num1), line_thick)
            if board[i][j] == 7:
                pygame.draw.line(screen, color, (mid_linex, y), (mid_linex, mid_liney), line_thick)
                pygame.draw.line(screen, color, (mid_linex, mid_liney), (x + num2, mid_liney), line_thick)
            if board[i][j] == 8:
                pygame.draw.line(screen, color, (mid_linex, y), (mid_linex, mid_liney), line_thick)
                pygame.draw.line(screen, color, (x, mid_liney), (mid_linex, mid_liney), line_thick)
            if board[i][j] == 9:
                pygame.draw.line(screen, 'white', (x, mid_liney),
                                 (x + num2, mid_liney), line_thick)


def draw_player():
    # 0 -> Right, 1 -> Left, 2 -> Up, 3 -> Down
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):

    turns = [False, False, False, False]
    fudge = 10
    # check collisions based on center x and center y of player +/- fudge number

    """x, y = centerx // num2, centery// num1
    x, y = x * num2 + (0.5 * num2), y * num1 + (0.5 * num1)
    print(x, y)"""

    if centerx // 30 < 19:
        if direction == 0:      # Right.
            if board[centery // num1][(centerx - fudge) // num2] < 3:
                turns[1] = True
        if direction == 1:      # Left
            if board[centery // num1][(centerx + fudge) // num2] < 3:
                turns[0] = True
        if direction == 2:      # Up
            if board[(centery + fudge) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:      # Down
            if board[(centery - fudge) // num1][(centerx - fudge) // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:     # 2 - UP, 3 - DOWN                        # y++ is going down
            if 5 <= centerx % num2 <= 15:                                                  # y-- is going up
                if board[(centery + fudge) // num1][centerx // num2] < 3:                  # xy(0, 0) is top left corner
                    turns[3] = True                                                        # of the screen
                if board[(centery - fudge) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 5 <= centery % num1 <= 15:
                if board[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if board[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 5 <= centerx % num2 <= 15:
                if board[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if board[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 5 <= centery % num1 <= 15:
                if board[centery // num1][(centerx - fudge) // num2] < 3:
                    turns[1] = True         # Left
                if board[centery // num1][(centerx + fudge) // num2] < 3:
                    turns[0] = True         # Right
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    #r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    if direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    if direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def check_collisions(score):
    x, y = center_x// num2, center_y//num1
    if 0 < player_x < WIDTH - 30:
        if board[y][x] == 1:
            board[y][x] = 0
            score += 10
        if board[y][x] == 2:
            board[y][x] = 0
            score += 50

    return score

def draw_misc():

    user_name = 'asdfasdf'
    score_text = font.render(f'Score: {scores}', True, 'white')
    name_txt = font.render(f'{user_name}', True, 'white')
    screen.blit(score_text, (0.5 * num2, (num1 + 5) // 2))  #score
    screen.blit(name_txt, (WIDTH - (name_txt.get_width() + num2), (num1 + 5) // 2)) #user name
    for i in range(2, 5):
        screen.blit(pygame.transform.scale(player_images[0], (20, 20)), (WIDTH - i * num2, HEIGHT - 25))


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')
    draw_board()
    draw_player()
    draw_misc()
    center_x = player_x + (num2 // 2)
    center_y = player_y + (num1 // 2)
    pygame.draw.circle(screen, 'red', [center_x, center_y], 2)
    turns_allowed = check_position(center_x, center_y)
    player_x, player_y = move_player(player_x, player_y)
    scores = check_collisions(scores)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            elif event.key == pygame.K_LEFT:
                direction_command = 1
            elif event.key == pygame.K_UP:
                direction_command = 2
            elif event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            elif event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            elif event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            elif event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i
    """if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
        """
    if player_x > 600:
        player_x = -10
    if player_x < -10:
        player_x = 600

    pygame.display.flip()
pygame.quit()
