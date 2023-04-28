import pygame
pygame.init()

"""def button(msg, x, y, w, h, inactive_color, active_color, active_scale, is_locked):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        scale_w = int(w * active_scale)
        scale_h = int(h * active_scale)
        x_offset = (scale_w - w) // 2
        y_offset = (scale_h - h) // 2
        pygame.draw.rect(screen, active_color, (x-x_offset, y-y_offset, scale_w, scale_h))
        if click[0] == 1:
            print("Button clicked")
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surface = font.render(msg, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (x+(w/2), y+(h/2))
    screen.blit(text_surface, text_rect)

    if is_locked:
        lock_image = pygame.image.load("level_menu_assets/images.png")
        resized_img = pygame.transform.scale(lock_image, (50, 50))
        screen.blit(resized_img, (button_x + i * button_spacing + 25, button_y + 40))"""

# Define some colors
def level_mmenu():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    Grey = (39, 41, 46)

    # Set the width and height of the screen
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Game Level Menu")

    # Define the font to be used
    font = pygame.font.SysFont(None, 36)


    # Set up the levels
    levels = [
        {"name": "Level 1", "locked": False},
        {"name": "Level 2", "locked": False},
        {"name": "Level 3", "locked": True},
    ]

    # Define the position of the first level button
    button_x = 200
    button_y = 200

    # Define the spacing between buttons
    button_spacing = 150

    # Loop until the user clicks the close button
    done = False

    # Main game loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on a level button
                mouse_pos = pygame.mouse.get_pos()
                for i, level in enumerate(levels):
                    button_rect = pygame.Rect(button_x + i * button_spacing, button_y, 150, 100)
                    if button_rect.collidepoint(mouse_pos):
                        if not level["locked"]:
                            # TODO: Start the selected level
                            # button entering level
                            print("Starting", level["name"])

                        elif level["locked"]:
                            # TODO: Display a message that the level is locked
                            print( level["name"], "is locked")

                back_button_rect = pygame.Rect(50, 500, 100, 50)
                if back_button_rect.collidepoint(mouse_pos):
                    done = True
                    print("going back to previous step")




        # Fill the background with Grey
        screen.fill(Grey)

        # Draw the level buttons
        for i, level in enumerate(levels):
            # Determine the position of the button
            button_rect = pygame.Rect(button_x + i * button_spacing, button_y, 100, 100)

            # Determine the button color based on whether it is locked or not
            if level["locked"]:
                button_color = BLACK
            else:
                button_color = (50, 50, 200)

            # Draw the button rectangle
            pygame.draw.rect(screen, button_color, button_rect)

            # Draw the button label
            button_label = font.render(level["name"], True, WHITE)
            screen.blit(button_label, (button_x + i * button_spacing+ 10, button_y  + 10))

            # If the button is locked, draw a lock symbol over it
            if level["locked"]:
                lock_image = pygame.image.load("assets/level_menu/images.png")
                resized_img = pygame.transform.scale(lock_image, (50, 50))
                screen.blit(resized_img, (button_x + i * button_spacing + 25, button_y + 40))

        title_surface = font.render("Level Menu", True, BLACK)
        # Calculate the position to center the title
        title_x = (800 - title_surface.get_width()) // 2
        title_y = 100  # adjust as needed

        # Draw the title onto the screen

        screen.blit(title_surface, (title_x, title_y))

        back_button_rect = pygame.Rect(50, 500, 100, 50)
        back_button_text = font.render("Back", True, WHITE)
        pygame.draw.rect(screen, BLACK, back_button_rect, border_radius=20)
        screen.blit(back_button_text, (70, 510))

        # Update the screen
        pygame.display.flip()



# Quit the game
#level_mmenu()
pygame.quit()
