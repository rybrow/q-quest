import pygame
import sys
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT

# Function to display title screen
def title_screen(screen):
    title_font = pygame.font.SysFont('Arial', 64, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 32)
    instruction_font = pygame.font.SysFont('Arial', 24)

    title_text = title_font.render("Q-Quest!", True, WHITE)
    subtitle_text = subtitle_font.render("An Epic Adventure", True, LIGHT_BLUE)
    instruction_text = instruction_font.render("Press SPACE to start or ESC to quit", True, WHITE)

    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))

    in_title_screen = True
    clock = pygame.time.Clock()

    while in_title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    in_title_screen = False

        # Create a gradient background
        for y in range(HEIGHT):
            # Calculate color gradient from dark blue to black
            color_value = max(0, 50 - y // 10)
            pygame.draw.line(screen, (0, 0, color_value), (0, y), (WIDTH, y))

        # Draw a decorative border
        pygame.draw.rect(screen, LIGHT_BLUE, (20, 20, WIDTH-40, HEIGHT-40), 3)

        # Draw title elements
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        screen.blit(instruction_text, instruction_rect)

        # Add a pulsing effect to the instruction text
        pulse = (pygame.time.get_ticks() % 1000) / 1000  # Value between 0 and 1
        pulse_value = int(128 + 127 * abs(pulse * 2 - 1))  # Pulsing between 128 and 255
        instruction_text = instruction_font.render("Press SPACE to start or ESC to quit", True, (pulse_value, pulse_value, pulse_value))

        pygame.display.flip()
        clock.tick(60)