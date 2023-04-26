# menu.py
import sqlite3
import pygame
import sys
from level_menu import level_menu

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_MENU = pygame.font.Font(None, 40)

# Set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man')


# Show scoreboard function
def show_scoreboard():
    # Set up the window
    size = [WIDTH, HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pacman Scores")

    # Set up the font
    font = pygame.font.Font(None, 32)

    # Set up the database connection
    conn = sqlite3.connect('pacman_scores.db')
    c = conn.cursor()

    # Get the scores from the database
    c.execute('SELECT username, score FROM scores ORDER BY score DESC')
    scores = c.fetchall()

    # Get the number of scores
    num_scores = len(scores)

    # Find the highest score and its associated username
    highest_score = None
    highest_username = None
    for score in scores:
        if highest_score is None or score[1] > highest_score:
            highest_score = score[1]
            highest_username = score[0]

    # Set up the table headers
    headers = ['Username', 'Score']

    # Set up the column widths
    col_widths = [300, 150]

    # Set up the starting position for the table
    x = 200
    y = 200
    row_spacing = 40

    # Draw the title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Scoreboard", True, (255, 255, 255))
    screen.blit(title_text, (300, 100))

    # Display the table headers
    header_x = x
    for i, header in enumerate(headers):
        header_text = font.render(header, True, (255, 255, 255))
        screen.blit(header_text, (header_x, y))
        header_x += col_widths[i]

    # Set up the row colors
    light_gray = (200, 200, 200)
    white = (255, 255, 255)
    row_colors = [white, light_gray]

    # Load the icon image
    icon_image = pygame.image.load('/Users/linhtetwin/Downloads/pac_man.png')
    icon = pygame.transform.scale(icon_image, (20, 20))

    # Display the scores in the table
    for i, score in enumerate(scores):
        # Determine the row color based on the row index
        row_color = row_colors[i % 2]

        # Display the username with the row color
        username_text = font.render(score[0], True, row_color)
        screen.blit(username_text, (x, y + (i + 1) * row_spacing))

        # Display the score with the row color
        score_text = font.render(str(score[1]), True, row_color)
        screen.blit(score_text, (x + col_widths[0], y + (i + 1) * row_spacing))

        # Check if this score is the highest score
        if score[1] == highest_score:
            # Render and blit the icon image
            icon_x = col_widths[1]  # add some padding
            icon_y = y
            screen.blit(icon, (icon_x, icon_y))

    # Add spacing between the header and data rows
    y += row_spacing

    # Load the icon image
    icon_image = pygame.image.load('/Users/linhtetwin/Downloads/back.png')
    icon = pygame.transform.scale(icon_image, (20, 20))

    # Set the color of the icon to white
    icon.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
    # Render and blit the icon image
    screen.blit(icon, (90, 440))

    # Add back button to go back to the menu
    back_option = FONT_MENU.render('Back', True, WHITE)
    back_rect = back_option.get_rect(center=(150, 450))
    screen.blit(back_option, back_rect)

    # Wait for the user to close the window
    show_score = True
    while show_score:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_rect = pygame.Rect((100,430,100,40))
                if back_rect.collidepoint(mouse_pos):
                    show_score = False

        # Update the screen
        pygame.display.update()

        pygame.time.wait(10)

def draw_menu():
    screen.fill(BLACK)

    title = FONT_MENU.render('Pac-Man', True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)

    play_option = FONT_MENU.render('Play', True, WHITE)
    play_rect = play_option.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(play_option, play_rect)

    score_option = FONT_MENU.render('Scoreboard', True, WHITE)
    score_rect = score_option.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 50))
    screen.blit(score_option, score_rect)

    exit_option = FONT_MENU.render('Exit', True, WHITE)
    exit_rect = exit_option.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 100))
    screen.blit(exit_option, exit_rect)

    pygame.display.flip()

def show_user():
    clock = pygame.time.Clock()

    # Set up the screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pacman")

    # Set up the database connection
    conn = sqlite3.connect('pacman_scores.db')
    c = conn.cursor()

    # Set up the font for the username text field
    base_font = pygame.font.Font(None, 32)
    user_text = ''

    # Set up the rectangle for the username text field
    input_rect = pygame.Rect(450, 250, 200, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    # Set up the font for the buttons
    button_font = pygame.font.Font(None, 24)

    # Set up the "Ok" button
    ok_button = pygame.Rect(350, 350, 80, 40)
    ok_text = button_font.render("Ok", True, (255, 255, 255))
    ok_text_rect = ok_text.get_rect(center=ok_button.center)

    # Set up the "Cancel" button
    cancel_button = pygame.Rect(450, 350, 80, 40)
    cancel_text = button_font.render("Cancel", True, (255, 255, 255))
    cancel_text_rect = cancel_text.get_rect(center=cancel_button.center)

    run = True
    # Game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if ok_button.collidepoint(event.pos):
                    if user_text.strip() != '':
                        # If there is username, add the username into database
                        c.execute("INSERT INTO scores (username,score) VALUES (?,?)", (user_text, 0))
                        conn.commit()
                        print("Database added successfully.")
                        level_menu()


                    else:
                        # Show an error message box
                        error_font = pygame.font.SysFont(None, 30)
                        error_text = error_font.render("Please enter a username.", True, (255, 0, 0))
                        screen.blit(error_text, (WIDTH / 2 - error_text.get_width() / 2, 550))
                        pygame.display.update()

                if cancel_button.collidepoint(event.pos):
                    run = False
                    print("Cancel button clicked")
                    user_text = ''

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_TAB:
                        continue
                    elif event.key == pygame.K_RETURN:
                        return user_text
                    else:
                        user_text += event.unicode

        # Draw the background
        screen.fill((0, 0, 0))

        # Draw the title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Pacman", True, (255, 255, 255))
        screen.blit(title_text, (350, 100))

        # Draw the username text field
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        # create the text object for "Type your username here"
        username_text = base_font.render("Type your username here", True, (255, 0, 0))
        screen.blit(username_text, (input_rect.x - 280, input_rect.y + 5))

        # Draw the buttons
        pygame.draw.rect(screen, (255, 0, 0), ok_button)
        pygame.draw.rect(screen, (0, 255, 0), cancel_button)
        screen.blit(ok_text, ok_text_rect)
        screen.blit(cancel_text, (cancel_button.x + 10, cancel_button.y + 10))

        pygame.display.update()
        clock.tick(60)
    # This line is only reached if the user closes the window without entering a username
    return None


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
                score_rect = pygame.Rect((WIDTH // 2) - 50, ((HEIGHT // 2) + 50) - 20, 100, 40)
                exit_rect = pygame.Rect((WIDTH // 2) - 50, ((HEIGHT // 2) + 100) - 20, 100, 40)

                if play_rect.collidepoint(mouse_pos):
                    username = show_user()
                    if username is not None:
                        menu = False
                elif score_rect.collidepoint(mouse_pos):
                    show_scoreboard()
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.time.Clock().tick(60)


def run_menu():
    menu_loop()