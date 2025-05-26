import json
import os
import pygame
import sys
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT

# Create a level selection screen
def level_selection_screen(screen):
    """Display a screen to select a level"""
    # Initialize Pygame if not already done
    if not pygame.get_init():
        pygame.init()

    # Set up display
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level Selection - Q-Quest!")

    # Load levels
    levels = load_levels()

    if not levels:
        print("No levels found!")
        return None

    # Create fonts
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    level_name_font = pygame.font.SysFont('Arial', 28, bold=True)
    description_font = pygame.font.SysFont('Arial', 20)

    # Create a level selection box class
    class LevelBox:
        def __init__(self, x, y, width, height, level_data):
            self.rect = pygame.Rect(x, y, width, height)
            self.level_data = level_data
            self.hovered = False

            # Load player image
            self.player_image = None
            try:
                player_image_path = os.path.join(level_data['directory'], level_data.get('player', {}).get('image', 'placeholder.png'))
                if os.path.exists(player_image_path):
                    self.player_image = pygame.image.load(player_image_path)
                    self.player_image = pygame.transform.scale(self.player_image, (128, 128))
                else:
                    # Try placeholder image
                    placeholder_path = os.path.join(level_data['directory'], 'placeholder.png')
                    if os.path.exists(placeholder_path):
                        self.player_image = pygame.image.load(placeholder_path)
                        self.player_image = pygame.transform.scale(self.player_image, (128, 128))
            except Exception as e:
                print(f"Error loading player image for {level_data['name']}: {e}")

        def draw(self, surface):
            # Draw box background with highlight if hovered
            color = DARK_GRAY
            if self.hovered:
                # Lighten the color when hovered
                color = tuple(min(c + 30, 255) for c in color)

            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)  # Border

            # Draw player image (left side)
            if self.player_image:
                surface.blit(self.player_image, (self.rect.x + 30, self.rect.y + (self.rect.height - 128) // 2))
            else:
                # Draw placeholder rectangle if no image
                pygame.draw.rect(surface, (100, 100, 100),
                                (self.rect.x + 30, self.rect.y + (self.rect.height - 128) // 2, 128, 128))

            # Draw level name (30px to the right of image, 20px from top)
            name_text = level_name_font.render(self.level_data['name'], True, WHITE)
            surface.blit(name_text, (self.rect.x + 30 + 128 + 30, self.rect.y + 20))

            # Draw level description (30px to the right of image, 25px below title)
            description = self.level_data.get('description', 'No description available')
            # Wrap text if too long
            words = description.split(' ')
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                # If line would be too long with this word, start a new line
                if description_font.size(test_line)[0] > self.rect.width - (30 + 128 + 30 + 30):
                    lines.append(line)
                    line = word + " "
                else:
                    line = test_line
            lines.append(line)  # Add the last line

            # Draw each line of the description (limit to 2 lines to fit in smaller box)
            max_lines = min(2, len(lines))
            for i in range(max_lines):
                desc_text = description_font.render(lines[i], True, WHITE)
                surface.blit(desc_text, (self.rect.x + 30 + 128 + 30, self.rect.y + 20 + 30 + i * 22))

            # Draw enemy count
            enemy_count = len(self.level_data.get('enemies', []))
            enemies_text = description_font.render(f"Enemies: {enemy_count}", True, WHITE)
            surface.blit(enemies_text, (self.rect.x + 30 + 128 + 30, self.rect.y + self.rect.height - 30))

        def check_hover(self, pos):
            self.hovered = self.rect.collidepoint(pos)
            return self.hovered

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    return True
            return False

    # Create back button
    class Button:
        def __init__(self, x, y, width, height, text, color=DARK_GRAY):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.hovered = False

        def draw(self, surface):
            # Draw button with highlight if hovered
            color = self.color
            if self.hovered:
                # Lighten the color when hovered
                color = tuple(min(c + 30, 255) for c in self.color)

            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)  # Border

            # Draw text
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

        def check_hover(self, pos):
            self.hovered = self.rect.collidepoint(pos)
            return self.hovered

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    return True
            return False

    # Create level boxes
    level_boxes = []
    box_height = 160  # Further reduced height to avoid overlap with back button
    box_width = WIDTH - 60  # 30px margin on each side
    box_margin = 15  # Margin between boxes

    for i, level in enumerate(levels):
        y_pos = 100 + i * (box_height + box_margin)  # Adjusted starting position
        box = LevelBox(30, y_pos, box_width, box_height, level)
        level_boxes.append((box, level))

    # Create back button
    back_button = Button(WIDTH - 150, HEIGHT - 80, 120, 40, "Back", DARK_GRAY)

    # Main loop
    running = True
    selected_level = None
    clock = pygame.time.Clock()

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Check button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box, level in level_boxes:
                    if box.handle_event(event):
                        selected_level = level
                        running = False

                if back_button.handle_event(event):
                    running = False

        # Update hover states
        for box, _ in level_boxes:
            box.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        # Create gradient background
        for y in range(HEIGHT):
            color_value = max(0, 50 - y // 10)
            pygame.draw.line(screen, (0, 0, color_value), (0, y), (WIDTH, y))

        # Draw title
        title_text = title_font.render("Select a Level", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))  # Moved title up slightly
        screen.blit(title_text, title_rect)

        # Draw level boxes
        for box, _ in level_boxes:
            box.draw(screen)

        # Draw back button
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return selected_level


# Add this function to load levels from the levels directory
def load_levels():
    """Load all level definitions from the levels directory"""
    levels = []
    levels_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "levels")

    if not os.path.exists(levels_dir):
        print(f"Levels directory not found: {levels_dir}")
        return levels

    # Iterate through each subdirectory in the levels directory
    for level_dir in os.listdir(levels_dir):
        level_path = os.path.join(levels_dir, level_dir)

        # Check if it's a directory and contains a level.json file
        if os.path.isdir(level_path):
            level_json_path = os.path.join(level_path, "level.json")

            if os.path.exists(level_json_path):
                try:
                    with open(level_json_path, 'r') as f:
                        level_data = json.load(f)

                    # Add the directory path to the level data
                    level_data['directory'] = level_path
                    level_data['file_path'] = level_json_path
                    levels.append(level_data)
                except Exception as e:
                    print(f"Error loading level from {level_json_path}: {e}")

    return levels
