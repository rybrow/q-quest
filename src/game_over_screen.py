import pygame
import sys
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT

def game_over_screen(screen, character_data, enemy_defeated, victory=False):
    """
    Display the game over screen.

    Args:
        screen: The pygame screen to draw on
        enemy_defeated: Number of enemies defeated
        victory: Whether the player won (True) or lost (False)

    Returns:
        bool: True to restart the game, False to quit
    """
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 64, bold=True)
    stats_font = pygame.font.SysFont('Arial', 32)
    instruction_font = pygame.font.SysFont('Arial', 24)

    # Set colors based on victory or defeat
    if victory:
        title_text = "VICTORY!"
        title_color = GREEN
        background_color = (0, 50, 0)  # Dark green background for victory
    else:
        title_text = "GAME OVER"
        title_color = RED
        background_color = (50, 0, 0)  # Dark red background for defeat

    # Create text surfaces
    game_over_text = title_font.render(title_text, True, title_color)

    # Create stats text
    if victory:
        stats_text = stats_font.render(f"Congratulations! You defeated all enemies!", True, WHITE)
    else:
        stats_text = stats_font.render(f"You were defeated!", True, WHITE)

    # Create instruction text
    restart_text = instruction_font.render("Press R to restart or ESC to quit", True, WHITE)

    # Get text rectangles for positioning
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    stats_rect = stats_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))

    # Main loop
    running = True
    clock = pygame.time.Clock()
    restart = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    restart = True
                    character_data['return_to_title'] = True  # Flag to return to level selection
                    running = False

        # Create a gradient background
        for y in range(HEIGHT):
            # Calculate color gradient
            if victory:
                # Green gradient for victory
                color_value = max(0, background_color[1] - y // 20)
                pygame.draw.line(screen, (0, color_value, 0), (0, y), (WIDTH, y))
            else:
                # Red gradient for defeat
                color_value = max(0, background_color[0] - y // 20)
                pygame.draw.line(screen, (color_value, 0, 0), (0, y), (WIDTH, y))

        # Draw decorative border
        border_color = GREEN if victory else RED
        pygame.draw.rect(screen, border_color, (20, 20, WIDTH-40, HEIGHT-40), 3)

        # Draw text
        screen.blit(game_over_text, game_over_rect)
        screen.blit(stats_text, stats_rect)
        screen.blit(restart_text, restart_rect)

        # Add a pulsing effect to the restart text
        pulse = (pygame.time.get_ticks() % 1000) / 1000  # Value between 0 and 1
        pulse_value = int(128 + 127 * abs(pulse * 2 - 1))  # Pulsing between 128 and 255
        restart_text = instruction_font.render("Press R to restart or ESC to quit", True, (pulse_value, pulse_value, pulse_value))

        pygame.display.flip()
        clock.tick(60)

    return restart
