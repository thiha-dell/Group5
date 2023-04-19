# menu.py
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_MENU = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man')


def draw_menu():
    screen.fill(BLACK)

    title = FONT_MENU.render('Pac-Man', True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)

    play_option = FONT_MENU.render('Play', True, WHITE)
    play_rect = play_option.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(play_option, play_rect)

    exit_option = FONT_MENU.render('Exit', True, WHITE)
    exit_rect = exit_option.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 50))
    screen.blit(exit_option, exit_rect)

    pygame.display.flip()


def menu_loop():
    menu = True

    while menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                play_rect = pygame.Rect((WIDTH // 2) - 50, (HEIGHT // 2) - 20, 100, 40)
                exit_rect = pygame.Rect((WIDTH // 2) - 50, ((HEIGHT // 2) + 50) - 20, 100, 40)

                if play_rect.collidepoint(mouse_pos):
                    menu = False
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.time.Clock().tick(60)


def run_menu():
    menu_loop()
