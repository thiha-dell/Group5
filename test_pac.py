import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the game objects
player_size = 20
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 5
player_direction = 'right'

wall_width = 20
walls = [
    pygame.Rect(0, 0, wall_width, screen_height),
    pygame.Rect(0, 0, screen_width, wall_width),
    pygame.Rect(screen_width - wall_width, 0, wall_width, screen_height),
    pygame.Rect(0, screen_height - wall_width, screen_width, wall_width),
    pygame.Rect(200, 150, wall_width, 150),
    pygame.Rect(400, 150, wall_width, 150),
]

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_direction = 'left'
            elif event.key == pygame.K_RIGHT:
                player_direction = 'right'
            elif event.key == pygame.K_UP:
                player_direction = 'up'
            elif event.key == pygame.K_DOWN:
                player_direction = 'down'

    # Move the player
    if player_direction == 'left':
        player_x -= player_speed
    elif player_direction == 'right':
        player_x += player_speed
    elif player_direction == 'up':
        player_y -= player_speed
    elif player_direction == 'down':
        player_y += player_speed

    # Check for collisions with walls
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for wall in walls:
        if player_rect.colliderect(wall):
            if player_direction == 'left':
                player_x += player_speed
            elif player_direction == 'right':
                player_x -= player_speed
            elif player_direction == 'up':
                player_y += player_speed
            elif player_direction == 'down':
                player_y -= player_speed

    # Draw the game objects
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 0), (player_x, player_y, player_size, player_size))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
