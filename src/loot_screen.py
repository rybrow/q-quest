import random
import pygame
import sys
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT, Button, draw_character_card
# from src.main import screen
from src.ui import calculate_card_height

# Game loop
# Function to display shop screen
def loot_screen(screen, character_data, enemy_data):
    """Loot screen where player can take items from defeated enemies"""
    # Initialize pygame if not already done
    if not pygame.get_init():
        pygame.init()

    # Define uniform margins (same as main game screen)
    margin = 30

    # Character card dimensions (same as main game screen)
    card_width = 300
    # Calculate item positions to determine required card height
    item_height = 30
    item_spacing = 10
    portrait_height = 256
    portrait_y = 60  # Below the name
    health_y = portrait_y + portrait_height + 20
    items_label_y = health_y + 30
    item_y_start = items_label_y + 30

    # Calculate the required card height
    card_height = calculate_card_height(item_y_start, item_height, item_spacing)

    # Define item card dimensions
    item_card_width = 200  # Width for loot item cards
    item_card_height = 150  # Height for loot item cards

    # Player card position (left side, top of screen)
    player_card_x = margin
    player_card_y = margin

    # Initialize player health for display
    player_health = character_data.get('health', 5)

    # Extract enemy items for looting
    enemy_items = enemy_data.get('items', {})

    # Initialize loot items (None if not available)
    attack_item = None
    defend_item = None
    heal_item = None

    # Check if enemy has each type of item
    if 'attack' in enemy_items and enemy_items.get('attack', {}).get('name'):
        attack_item = {
            'name': enemy_items['attack']['name'],
            'modifier': enemy_items['attack']['modifier'],
            'type': 'ATTACK',
            'cost': enemy_items['attack']['modifier'] * 20  # Cost based on modifier
        }

    if 'defense' in enemy_items and enemy_items.get('defense', {}).get('name'):
        defend_item = {
            'name': enemy_items['defense']['name'],
            'modifier': enemy_items['defense']['modifier'],
            'type': 'DEFEND',
            'cost': enemy_items['defense']['modifier'] * 20  # Cost based on modifier
        }

    if 'heal' in enemy_items and enemy_items.get('heal', {}).get('name'):
        heal_item = {
            'name': enemy_items['heal']['name'],
            'modifier': enemy_items['heal']['modifier'],
            'type': 'HEAL',
            'cost': enemy_items['heal']['modifier'] * 20  # Cost based on modifier
        }

    # Create list of available loot items (filtering out None values)
    loot_items = [item for item in [attack_item, defend_item, heal_item] if item is not None]

    # Create UI elements
    header_font = pygame.font.SysFont('Arial', 42, bold=True)
    item_font = pygame.font.SysFont('Arial', 24, bold=True)
    description_font = pygame.font.SysFont('Arial', 18)

    # Create done button
    done_button = Button(WIDTH - 150, HEIGHT - 60, 120, 40, "Done", DARK_GRAY)

    # Message display variables
    message = ""
    message_color = WHITE
    message_timer = 0

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)  # Clear screen

        # Draw player card
        draw_character_card(screen, character_data, player_card_x, player_card_y, card_width, card_height, player_health)

        # Draw loot items
        loot_title = header_font.render("Enemy Loot", True, WHITE)
        loot_title_rect = loot_title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(loot_title, loot_title_rect)

        # Draw instructions
        instructions = description_font.render("Click on an item to add it to your inventory", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, 140))
        screen.blit(instructions, instructions_rect)

        # Draw loot items
        if not loot_items:
            # No items to loot
            no_items_text = item_font.render("No items to loot", True, WHITE)
            no_items_rect = no_items_text.get_rect(center=(WIDTH // 2, 200))
            screen.blit(no_items_text, no_items_rect)
        else:
            # Calculate positions for loot items
            # Ensure first item is at least 60px to the right of character card
            min_start_x = player_card_x + card_width + 60
            
            # Calculate total width needed for all items with spacing
            item_spacing = 30  # Increased spacing between items
            total_width = len(loot_items) * item_card_width + (len(loot_items) - 1) * item_spacing
            
            # Center the items in the remaining space
            remaining_width = WIDTH - min_start_x - margin
            start_x = min_start_x + (remaining_width - total_width) // 2
            
            # Ensure start_x is at least min_start_x
            start_x = max(start_x, min_start_x)

            # Draw each loot item
            for i, item in enumerate(loot_items):
                item_x = start_x + i * (item_card_width + item_spacing)
                item_y = 200

                # Draw item card background
                if item['type'] == 'ATTACK':
                    card_color = RED
                elif item['type'] == 'DEFEND':
                    card_color = BLUE
                else:  # HEAL
                    card_color = GREEN

                # Draw card
                pygame.draw.rect(screen, DARK_GRAY, (item_x, item_y, item_card_width, item_card_height))
                pygame.draw.rect(screen, card_color, (item_x, item_y, item_card_width, item_card_height), 3)

                # Draw item name
                name_text = item_font.render(item['name'], True, WHITE)
                name_rect = name_text.get_rect(center=(item_x + item_card_width // 2, item_y + 30))
                screen.blit(name_text, name_rect)

                # Draw item type
                type_text = description_font.render(item['type'], True, WHITE)
                type_rect = type_text.get_rect(center=(item_x + item_card_width // 2, item_y + 60))
                screen.blit(type_text, type_rect)

                # Draw modifier
                mod_text = description_font.render(f"Modifier: +{item['modifier']}", True, WHITE)
                mod_rect = mod_text.get_rect(center=(item_x + item_card_width // 2, item_y + 90))
                screen.blit(mod_text, mod_rect)

                # Check if mouse is over this item
                item_rect = pygame.Rect(item_x, item_y, item_card_width, item_card_height)
                if item_rect.collidepoint(pygame.mouse.get_pos()):
                    # Highlight the item
                    pygame.draw.rect(screen, WHITE, (item_x, item_y, item_card_width, item_card_height), 2)

                    # Show "Click to take" text
                    take_text = description_font.render("Click to take", True, WHITE)
                    take_rect = take_text.get_rect(center=(item_x + item_card_width // 2, item_y + 120))
                    screen.blit(take_text, take_rect)

        # Draw done button
        done_button.draw(screen)

        # Draw message if present
        if message and message_timer > 0:
            message_font = pygame.font.SysFont('Arial', 24, bold=True)
            message_text = message_font.render(message, True, message_color)
            message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            screen.blit(message_text, message_rect)
            message_timer -= 1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a loot item was clicked
                if loot_items:  # Only check if there are items
                    for i, item in enumerate(loot_items):
                        item_x = start_x + i * (item_card_width + item_spacing)
                        item_y = 200
                        item_rect = pygame.Rect(item_x, item_y, item_card_width, item_card_height)

                        if item_rect.collidepoint(event.pos):
                            # Add the item to player's inventory
                            if item['type'] == 'ATTACK':
                                character_data['items']['attack'] = {
                                    'name': item['name'],
                                    'modifier': item['modifier']
                                }
                                message = f"Added {item['name']} to your inventory!"
                                message_color = GREEN
                            elif item['type'] == 'DEFEND':
                                character_data['items']['defense'] = {
                                    'name': item['name'],
                                    'modifier': item['modifier']
                                }
                                message = f"Added {item['name']} to your inventory!"
                                message_color = GREEN
                            elif item['type'] == 'HEAL':
                                character_data['items']['heal'] = {
                                    'name': item['name'],
                                    'modifier': item['modifier']
                                }
                                message = f"Added {item['name']} to your inventory!"
                                message_color = GREEN

                            # Remove the item from loot
                            loot_items.pop(i)
                            message_timer = 120  # Show message for 2 seconds (60 fps * 2)

                            # Exit loot screen after adding item to inventory
                            running = False
                            break

                # Check if done button was clicked
                if done_button.handle_event(event):
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    running = False

        pygame.display.flip()
        clock.tick(60)

    # Set flag to return to map
    character_data['return_to_map'] = True
    return character_data
