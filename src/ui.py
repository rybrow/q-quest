import pygame
import os
import pytmx


WIDTH = 1280
HEIGHT = 720

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (170, 170, 255)


# Function to calculate the required card height
def calculate_card_height(item_y_start, item_height, item_spacing):
    # Calculate the height needed for the card based on content
    # Base height includes: portrait (256px) + margins and spacing + 3 items + gold label + bottom margin
    currency_y = item_y_start + 3 * (item_height + item_spacing) + 30  # Same calculation as in draw_character_card
    return currency_y + 60  # Add 60px below the gold label for more space


# Button class for UI interactions
class Button:
    def __init__(self, x, y, width, height, text, color=DARK_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.font = pygame.font.SysFont('Arial', 24)
        self.is_hovered = False
        self.is_selected = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        # Determine color based on state
        if self.is_selected:
            color = HIGHLIGHT
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color

        # Draw button
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


# Function to draw character card with multiple items and currency
def draw_character_card(surface, character_data, x, y, width, height, health_level=5, is_enemy=False, image_path=None):
    # Draw card background with gradient
    for i in range(height):
        color_value = max(0, 30 - i // 10)
        pygame.draw.line(surface, (0, 0, color_value), (x, y + i), (x + width, y + i))

    # Draw card border
    border_color = RED if is_enemy else LIGHT_BLUE
    pygame.draw.rect(surface, border_color, (x, y, width, height), 3)

    # Draw character name

    # Draw character portrait

    # Draw portrait placeholder (256x256) centered horizontally
    portrait_width = 256
    portrait_height = 256
    portrait_x = x + (width - portrait_width) // 2
    portrait_y = y + 60  # Below the name

    try:
        # Get image path from character_data if not provided
        if image_path is None:
            level_dir = character_data['level'].get('directory', '')
            image_path = f"{level_dir}/{character_data.get('image', None)}"

        # If still no image path, use global default
        if image_path is None:
            image_path = "images/placeholder.png"

        # Load and display portrait
        portrait = pygame.image.load(image_path)

        portrait = pygame.transform.scale(portrait, (portrait_width, portrait_height))
        surface.blit(portrait, (portrait_x, portrait_y))

        # Adjust y position for health bar to be below portrait
        health_y = portrait_y + portrait_height + 10
    except Exception as e:
        print(f"Error loading portrait: {e}")
        # Use a placeholder rectangle if image can't be loaded
        portrait_width = width - 20
        portrait_height = height // 3
        pygame.draw.rect(surface, (100, 100, 100), (x + 10, y + 40, portrait_width, portrait_height))
        health_y = y + 40 + portrait_height + 10

    name_font = pygame.font.SysFont('Arial', 28, bold=True)
    name_text = name_font.render(character_data["name"], True, WHITE)
    name_rect = name_text.get_rect(center=(x + width//2, y + 30))
    surface.blit(name_text, name_rect)

    # Draw segmented health bar below portrait
    health_y = portrait_y + portrait_height + 20
    draw_segmented_health_bar(
        surface,
        x + 20,                # x position
        health_y,              # y position
        width - 40,            # width
        20,                    # height
        5,                     # total segments
        health_level,          # current filled segments
        WHITE,                 # border color
        GREEN,                 # fill color
        DARK_GRAY,             # empty segment color
        BLACK                  # background color
    )

    # Draw "Items:" label
    items_label_y = health_y + 30
    items_font = pygame.font.SysFont('Arial', 22, bold=True)
    items_text = items_font.render("Items:", True, WHITE)
    items_rect = items_text.get_rect(midleft=(x + 20, items_label_y + 10))
    surface.blit(items_text, items_rect)

# Calculate spacing for items
    item_height = 30
    item_spacing = 10
    item_y_start = items_label_y + 30

    # For enemies, keep the old display method
    if is_enemy:
        # Check if enemy has the new items structure
        if "items" in character_data:
            items = character_data["items"]

            # Draw attack item (first slot)
            if "attack" in items and items["attack"]["name"]:
                draw_item_button(
                    surface,
                    x + 20,                # x position
                    item_y_start,          # y position
                    width - 40,            # width
                    item_height,           # height
                    items["attack"]["name"],
                    items["attack"]["modifier"],
                    "ATTACK"
                )
            else:
                # Draw empty attack slot
                pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start, width - 40, item_height))
                pygame.draw.rect(surface, GRAY, (x + 20, item_y_start, width - 40, item_height), 1)
                slot_font = pygame.font.SysFont('Arial', 16)
                slot_text = slot_font.render("Empty Slot", True, GRAY)
                slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + item_height//2))
                surface.blit(slot_text, slot_rect)

            # Draw defense item (second slot)
            if "defense" in items and items["defense"]["name"]:
                draw_item_button(
                    surface,
                    x + 20,                # x position
                    item_y_start + (item_height + item_spacing),  # y position
                    width - 40,            # width
                    item_height,           # height
                    items["defense"]["name"],
                    items["defense"]["modifier"],
                    "DEFEND"
                )
            else:
                # Draw empty defense slot
                pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start + (item_height + item_spacing), width - 40, item_height))
                pygame.draw.rect(surface, GRAY, (x + 20, item_y_start + (item_height + item_spacing), width - 40, item_height), 1)
                slot_font = pygame.font.SysFont('Arial', 16)
                slot_text = slot_font.render("Empty Slot", True, GRAY)
                slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + (item_height + item_spacing) + item_height//2))
                surface.blit(slot_text, slot_rect)

            # Draw heal item (third slot)
            if "heal" in items and items["heal"]["name"]:
                draw_item_button(
                    surface,
                    x + 20,                # x position
                    item_y_start + 2 * (item_height + item_spacing),  # y position
                    width - 40,            # width
                    item_height,           # height
                    items["heal"]["name"],
                    items["heal"]["modifier"],
                    "HEAL"
                )
            else:
                # Draw empty heal slot
                pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start + 2 * (item_height + item_spacing), width - 40, item_height))
                pygame.draw.rect(surface, GRAY, (x + 20, item_y_start + 2 * (item_height + item_spacing), width - 40, item_height), 1)
                slot_font = pygame.font.SysFont('Arial', 16)
                slot_text = slot_font.render("Empty Slot", True, GRAY)
                slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + 2 * (item_height + item_spacing) + item_height//2))
                surface.blit(slot_text, slot_rect)

        # Legacy support for old enemy format
        elif "item_name" in character_data and "item_type" in character_data and "item_modifier" in character_data:
            # Main item
            draw_item_button(
                surface,
                x + 20,                # x position
                item_y_start,          # y position
                width - 40,            # width
                item_height,           # height
                character_data["item_name"],
                character_data["item_modifier"],
                character_data["item_type"]
            )

            # Placeholder for additional items (if we had them)
            # For now, we'll draw empty slots
            for i in range(1, 3):
                pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start + i * (item_height + item_spacing), width - 40, item_height))
                pygame.draw.rect(surface, GRAY, (x + 20, item_y_start + i * (item_height + item_spacing), width - 40, item_height), 1)

                # Draw "Empty Slot" text
                slot_font = pygame.font.SysFont('Arial', 16)
                slot_text = slot_font.render("Empty Slot", True, GRAY)
                slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + i * (item_height + item_spacing) + item_height//2))
                surface.blit(slot_text, slot_rect)
    else:
        # For player, show all three item slots
        # Draw attack item
        if "items" in character_data and character_data["items"].get("attack", False):
        # if "attack_item" in character_data and character_data["attack_item"]["name"]:
            draw_item_button(
                surface,
                x + 20,                # x position
                item_y_start,          # y position
                width - 40,            # width
                item_height,           # height
                character_data["items"]["attack"]["name"],
                character_data["items"]["attack"]["modifier"],
                "ATTACK"
            )
        else:
            # Draw empty attack slot
            pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start, width - 40, item_height))
            pygame.draw.rect(surface, RED, (x + 20, item_y_start, width - 40, item_height), 1)
            slot_font = pygame.font.SysFont('Arial', 16)
            slot_text = slot_font.render("No Attack Item", True, RED)
            slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + item_height//2))
            surface.blit(slot_text, slot_rect)

        # Draw defend item
        if "items" in character_data and character_data["items"].get("defense", False):
        # if "defend_item" in character_data and character_data["defend_item"]["name"]:
            draw_item_button(
                surface,
                x + 20,                # x position
                item_y_start + item_height + item_spacing,  # y position
                width - 40,            # width
                item_height,           # height
                character_data["items"]["defense"]["name"],
                character_data["items"]["defense"]["modifier"],
                "DEFEND"
            )
        else:
            # Draw empty defend slot
            pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start + item_height + item_spacing, width - 40, item_height))
            pygame.draw.rect(surface, BLUE, (x + 20, item_y_start + item_height + item_spacing, width - 40, item_height), 1)
            slot_font = pygame.font.SysFont('Arial', 16)
            slot_text = slot_font.render("No Defend Item", True, BLUE)
            slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + item_height + item_spacing + item_height//2))
            surface.blit(slot_text, slot_rect)

        # Draw heal item
        if "items" in character_data and character_data["items"].get("heal", False):
        # if "heal_item" in character_data and character_data["heal_item"]["name"]:
            draw_item_button(
                surface,
                x + 20,                # x position
                item_y_start + 2 * (item_height + item_spacing),  # y position
                width - 40,            # width
                item_height,           # height
                character_data["items"]["heal"]["name"],
                character_data["items"]["heal"]["modifier"],
                "HEAL"
            )
        else:
            # Draw empty heal slot
            pygame.draw.rect(surface, DARK_GRAY, (x + 20, item_y_start + 2 * (item_height + item_spacing), width - 40, item_height))
            pygame.draw.rect(surface, GREEN, (x + 20, item_y_start + 2 * (item_height + item_spacing), width - 40, item_height), 1)
            slot_font = pygame.font.SysFont('Arial', 16)
            slot_text = slot_font.render("No Heal Item", True, GREEN)
            slot_rect = slot_text.get_rect(center=(x + width//2, item_y_start + 2 * (item_height + item_spacing) + item_height//2))
            surface.blit(slot_text, slot_rect)

    # Draw currency at the bottom with "Gold: " label
    currency_font = pygame.font.SysFont('Arial', 24, bold=True)
    currency_text = currency_font.render(f"Gold: {character_data.get('currency', 0)}", True, YELLOW)

    # Position currency 30px below the heal item
    currency_y = item_y_start + 3 * (item_height + item_spacing) + 30
    currency_rect = currency_text.get_rect(center=(x + width//2, currency_y))
    surface.blit(currency_text, currency_rect)
    # Character creation screen function


# Function to create an item button
def draw_item_button(surface, x, y, width, height, item_name, item_modifier, item_type):
    # Determine button color based on item type
    button_color = RED
    if item_type == "DEFEND":
        button_color = BLUE
    elif item_type == "HEAL":
        button_color = GREEN

    # Draw button background
    pygame.draw.rect(surface, button_color, (x, y, width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)

    # Draw button text
    font = pygame.font.SysFont('Arial', 20)
    text = font.render(f"{item_name} (+{item_modifier})", True, WHITE)
    text_rect = text.get_rect(center=(x + width//2, y + height//2))
    surface.blit(text, text_rect)

# Function to draw a segmented health bar
def draw_segmented_health_bar(surface, x, y, width, height, segments, current_segments, border_color=WHITE, fill_color=GREEN, empty_color=DARK_GRAY, background_color=BLACK):
    # Draw background
    pygame.draw.rect(surface, background_color, (x, y, width, height))

    # Calculate segment width (with small gap between segments)
    gap = 2
    segment_width = (width - (gap * (segments - 1))) / segments

    # Draw each segment
    for i in range(segments):
        segment_x = x + (i * (segment_width + gap))

        # Determine if this segment should be filled
        if i < current_segments:
            segment_color = fill_color
        else:
            segment_color = empty_color

        # Draw the segment
        pygame.draw.rect(surface, segment_color, (segment_x, y, segment_width, height))

    # Draw border around entire health bar
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)


def draw_minimap(surface, character_data, player_x, player_y, tmx_data, map_path):
    """
    Draw a minimap in the bottom right corner of the screen
    
    Args:
        surface: The main screen surface to draw on
        character_data: Player character data containing level and enemy info
        player_x: Current player X position on the map
        player_y: Current player Y position on the map
        tmx_data: The loaded TMX map data
        map_path: Path to the TMX map file
    """
    # Import here to avoid circular imports
    from src.map_renderer import render_map_to_surface
    
    # Minimap dimensions and position
    minimap_size = 200
    margin = 20
    minimap_x = WIDTH - minimap_size - margin
    minimap_y = HEIGHT - minimap_size - margin
    
    # Simple caching mechanism - store the base minimap surface
    if not hasattr(draw_minimap, 'cache'):
        draw_minimap.cache = {}
    
    cache_key = map_path
    
    try:
        # Get or create the base minimap surface
        if cache_key not in draw_minimap.cache:
            print(f"Creating minimap cache for: {map_path}")
            base_minimap = render_map_to_surface(map_path, minimap_size, minimap_size)
            draw_minimap.cache[cache_key] = base_minimap
        else:
            base_minimap = draw_minimap.cache[cache_key]
        
        # Create a working copy for this frame
        overlay = pygame.Surface((minimap_size, minimap_size))
        overlay.set_alpha(200)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Black background
        
        # Blit the cached base map onto the overlay
        base_minimap.set_alpha(180)
        overlay.blit(base_minimap, (0, 0))
        
        # Calculate scale factors for positioning dots
        if tmx_data:
            scale_x = minimap_size / tmx_data.width
            scale_y = minimap_size / tmx_data.height
            
            # Draw enemy positions as red dots
            if 'level' in character_data and 'enemies' in character_data['level']:
                for enemy in character_data['level']['enemies']:
                    if 'position' in enemy:
                        enemy_x = enemy['position'].get('x', 0)
                        enemy_y = enemy['position'].get('y', 0)
                        
                        # Convert map coordinates to minimap coordinates
                        dot_x = int(enemy_x * scale_x)
                        dot_y = int(enemy_y * scale_y)
                        
                        # Draw red dot for enemy (with white border for visibility)
                        pygame.draw.circle(overlay, WHITE, (dot_x, dot_y), 4)
                        pygame.draw.circle(overlay, RED, (dot_x, dot_y), 3)
            
            # Draw player position as green dot
            player_dot_x = int(player_x * scale_x)
            player_dot_y = int(player_y * scale_y)
            
            # Draw green dot for player (with white border for visibility)
            pygame.draw.circle(overlay, WHITE, (player_dot_x, player_dot_y), 5)
            pygame.draw.circle(overlay, GREEN, (player_dot_x, player_dot_y), 4)
        
        # Draw the minimap on the main surface
        surface.blit(overlay, (minimap_x, minimap_y))
        
        # Draw border around minimap
        pygame.draw.rect(surface, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Draw minimap title
        font = pygame.font.SysFont('Arial', 14, bold=True)
        title_text = font.render("Map", True, WHITE)
        title_rect = title_text.get_rect(center=(minimap_x + minimap_size // 2, minimap_y - 10))
        surface.blit(title_text, title_rect)
        
    except Exception as e:
        print(f"Error drawing minimap: {e}")
        # Draw a simple placeholder if minimap fails
        placeholder = pygame.Surface((minimap_size, minimap_size))
        placeholder.fill((50, 50, 50))
        surface.blit(placeholder, (minimap_x, minimap_y))
        pygame.draw.rect(surface, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Draw error text
        font = pygame.font.SysFont('Arial', 12)
        error_text = font.render("Minimap Error", True, RED)
        error_rect = error_text.get_rect(center=(minimap_x + minimap_size // 2, minimap_y + minimap_size // 2))
        surface.blit(error_text, error_rect)
