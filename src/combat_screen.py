import random
import pygame
import sys
from src import game_over_screen
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT, draw_character_card
from src.ui import calculate_card_height, Button

def main_game_screen(screen, character_data):
    running = True
    clock = pygame.time.Clock()
    print("\n==== MAIN GAME SCREEN ====")
    print(f"Character data type: {type(character_data)}")
    if isinstance(character_data, dict):
        print(f"Character data keys: {character_data.keys()}")
        if 'current_enemy' in character_data:
            print(f"Current enemy: {character_data['current_enemy']}")
        if 'level' in character_data:
            print(f"Level data keys: {character_data['level'].keys() if isinstance(character_data['level'], dict) else type(character_data['level'])}")
            if isinstance(character_data['level'], dict) and 'player' in character_data['level']:
                print(f"Player data in level: {character_data['level']['player']}")


    # Define uniform margins
    margin = 30

    # Character card dimensions
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
    card_height = calculate_card_height(item_y_start, item_height, item_spacing)  # Increased height to fit all items  # Each card takes 50% of available height

    # Player card position (left side, top of screen)
    player_card_x = margin
    player_card_y = margin

    # Add currency to player data
    character_data['currency'] = 100  # Starting gold

    # Get enemy data from map collision or generate a random one
    if 'current_enemy' in character_data and character_data.get('start_combat', False):
        # Use the enemy from the map collision
        enemy_data = character_data.get('current_enemy', {'name': 'Unknown Enemy', 'health': 50, 'attack': 8})
    else:
        # Create a default enemy if none is provided
        enemy_data = {'name': 'Unknown Enemy', 'health': 50, 'attack': 8}

    enemy_data['level'] = character_data['level']

    # Add missing fields that are required for combat
    if 'currency' not in enemy_data:
        # Use item_modifier if available, otherwise use 1
        default_modifier = enemy_data.get('item_modifier', 1)
        enemy_data['currency'] = 10 * default_modifier

    # Handle items in the new format
    if 'items' not in enemy_data:
        enemy_data['items'] = {}
    # Handle items in the new format
    if 'items' not in enemy_data:
        enemy_data['items'] = {}

    # Get items, ensuring it's a dictionary
    items = enemy_data['items']
    if not isinstance(items, dict):
        print(f"Warning: enemy items is not a dictionary: {items}")
        # Convert to dictionary if possible
        if isinstance(items, list):
            # Convert list of items to dictionary
            items_dict = {}
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    item_type = item.get('type', f'item{i}').lower()
                    items_dict[item_type] = item
            enemy_data['items'] = items_dict
            items = items_dict
        else:
            # Create empty dictionary
            enemy_data['items'] = {}
            items = {}



    # Set the active item for display in the encounter message
    # Use the attack item for the encounter message
    # Set the active item for display in the encounter message
    # Use the attack item for the encounter message if available
    try:
        if isinstance(items, dict) and 'attack' in items:
            active_item = items['attack']
            enemy_data['item_name'] = active_item.get('name', 'Unknown Weapon')
            enemy_data['item_type'] = 'ATTACK'
            enemy_data['item_modifier'] = active_item.get('modifier', 1)
        else:
            # Create default item data if not available
            enemy_data['item_name'] = 'Fists'
            enemy_data['item_type'] = 'ATTACK'
            enemy_data['item_modifier'] = 1
    except Exception as e:
        print(f"Error processing enemy items: {e}")
        # Create default item data if there's an error
        enemy_data['item_name'] = 'Fists'
        enemy_data['item_type'] = 'ATTACK'
        enemy_data['item_modifier'] = 1


    # Clear the start_combat flag
    character_data['start_combat'] = False
    print(f"Starting combat with {enemy_data['name']} wielding a {enemy_data['item_name']}")
    # Enemy card position (right side, top of screen)
    enemy_card_x = WIDTH - card_width - margin
    enemy_card_y = margin

    # Game area position and dimensions
    game_area_x = card_width + (2 * margin)
    game_area_width = WIDTH - (2 * card_width) - (4 * margin)
    game_area_y = margin
    game_area_height = card_height  # Match the height of the character cards

    # Action buttons dimensions
    button_height = 50
    button_width = 120
    button_y = HEIGHT - margin - button_height

    # Create action buttons
    # Position buttons 30px below the enemy card and 30px above the outside box
    button_y = enemy_card_y + card_height + 30

    # Create instruction label
    label_font = pygame.font.SysFont('Arial', 18)
    instruction_label = label_font.render("Select Action and click Submit", True, WHITE)

    # Create buttons (keeping horizontal positions)
    # Create buttons with new positions - removed submit button
    attack_button = Button(game_area_x, button_y, button_width, button_height, "Attack", RED)
    heal_button = Button(game_area_x + button_width + 30, button_y, button_width, button_height, "Heal", GREEN)
    run_button = Button(game_area_x + game_area_width - button_width, button_y, button_width, button_height, "Run", DARK_GRAY)


    # Track selected action
    selected_action = None
    action_buttons = [attack_button, heal_button]

    # Action log
    action_log = ["Welcome to Q-Quest! Your adventure begins...",
                 f"You encounter a {enemy_data['name']}!"]

    # Health levels (1-5)
    # Initialize health
    player_health = character_data.get("health", 5)  # Get health from character_data or default to 5
    character_data["health"] = player_health  # Store health in character_data
    enemy_health = enemy_data.get('health', 50)
    enemy_max_health = enemy_data.get('max_health', enemy_health)
    enemy_attack = enemy_data.get('attack', 8)
    enemy_defense = enemy_data.get('defense', 3)
    enemy_defeated = 0  # Counter for defeated enemies

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check run button
                if run_button.is_clicked(mouse_pos):
                    print("Running from combat...")
                    # Make sure pre_combat_position is preserved
                    if 'pre_combat_position' not in character_data:
                        print("WARNING: pre_combat_position not found!")
                    else:
                        print(f"Run button clicked, pre_combat_position: {character_data['pre_combat_position']}")
                    # Set flag to return to map
                    character_data['return_to_map'] = True
                    print(f"Character Data after setting return_to_map: {type(character_data)}")
                    print(f"Setting return_to_map flag, pre_combat_position: {character_data.get('pre_combat_position')}")
                    # End combat
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Allow Enter or Space to continue to the main game
                    running = False
                elif event.key == pygame.K_s:
                    # Open shop when S key is pressed
                    # Loot screen requires an enemy, so this is disabled
                    pass  # No action needed
                    # No need to reset the screen

            # Handle action button events
            for i, button in enumerate(action_buttons):
                if button.handle_event(event):
                    # Execute action immediately instead of just selecting it
                    selected_action = ["ATTACK", "HEAL"][i]

                    # Perform the selected action
                    if selected_action == "ATTACK":
                        # Get player's attack modifier from attack item
                        player_attack_mod = character_data['items'].get('attack', {}).get('modifier',0)

                        # Get enemy's defense modifier
                        enemy_defense_mod = character_data['items'].get('defense', {}).get('modifier',0)

                        # Roll for attack and defense
                        player_roll1, player_roll2, player_attack = roll_dice(player_attack_mod)
                        enemy_roll1, enemy_roll2, enemy_defense = roll_dice(enemy_defense_mod)

                        # Log the attack attempt
                        action_log.append(f"{character_data['name']} attacks with {character_data['items'].get('attack', {}).get('name', 'bare hands')}!")

                        # Determine if attack is successful and calculate damage tier
                        if player_attack >= enemy_defense:
                            # Calculate margin of success
                            margin = player_attack - enemy_defense

                            # Determine damage based on margin
                            damage = 1  # Base damage
                            if margin >= 6:
                                damage = 3  # Critical hit
                                action_log.append(f"CRITICAL HIT! {enemy_data['name']} takes {damage} damage!")
                            elif margin >= 3:
                                damage = 2  # Strong hit
                                action_log.append(f"Strong hit! {enemy_data['name']} takes {damage} damage!")
                            else:
                                action_log.append(f"Hit! {enemy_data['name']} takes {damage} damage!")

                            # Apply damage
                            enemy_health = max(0, enemy_health - damage)

                            # Check if enemy is defeated
                            if enemy_health <= 0:
                                # Calculate gold reward
                                # Calculate gold reward
                                gold_reward = enemy_data['currency'] + (5 * enemy_data['item_modifier'])
                                character_data['currency'] += gold_reward

                                # Mark the enemy as defeated in the level data
                                if 'level' in character_data and 'enemies' in character_data['level']:
                                    enemy_position = enemy_data.get('position', {})
                                    if enemy_position:
                                        # Find and remove the defeated enemy from the level's enemies list
                                        for i, e in enumerate(character_data['level']['enemies']):
                                            e_pos = e.get('position', {})
                                            if e_pos.get('x') == enemy_position.get('x') and e_pos.get('y') == enemy_position.get('y'):
                                                # Remove this enemy from the list
                                                character_data['level']['enemies'].pop(i)
                                                print(f"Removed defeated enemy at position {enemy_position}")
                                                break

                                # Check if all enemies are defeated
                                if 'level' in character_data and 'enemies' in character_data['level'] and len(character_data['level']['enemies']) == 0:
                                    # All enemies defeated - show victory screen
                                    print("All enemies defeated! Victory!")
                                    if game_over_screen.game_over_screen(screen, character_data, enemy_defeated, victory=True):
                                        # Return to level selection
                                        character_data['return_to_title'] = True
                                        return character_data
                                    else:
                                        running = False
                                        return False

                                # Set flag to return to map after combat
                                character_data['return_to_map'] = True

                                # Check if enemy has items to loot
                                has_items = False
                                if 'items' in enemy_data:
                                    items = enemy_data['items']
                                    if ('attack' in items and items.get('attack', {}).get('name')) or \
                                       ('defense' in items and items.get('defense', {}).get('name')) or \
                                       ('heal' in items and items.get('heal', {}).get('name')):
                                        has_items = True

                                # Store player health in character_data
                                character_data['health'] = player_health

                                if has_items:
                                    # Exit combat loop immediately to avoid flash
                                    # We'll show loot screen from main game loop
                                    character_data['show_loot'] = True  # Flag to show loot screen
                                    character_data['loot_enemy'] = enemy_data  # Store enemy for loot screen
                                    running = False
                                else:
                                    # No items to loot, end combat and return to map
                                    running = False

                                    # No items to loot, end combat and return to map
                                    running = False

                                # Store player health in character_data
                                character_data['health'] = player_health

                            elif enemy_health == 1:
                                action_log.append(f"{enemy_data['name']} is critically wounded!")
                        else:
                            # Attack fails
                            action_log.append(f"Attack fails! {enemy_data['name']} dodges the attack!")

                    elif selected_action == "HEAL":
                        # Check if player has a healing item
                        if character_data['items'].get('heal',False):
                            # Roll for healing effectiveness
                            heal_roll1, heal_roll2, heal_total = roll_dice(character_data['items']['heal']['modifier'])

                            # Log the healing attempt
                            action_log.append(f"{character_data['name']} attempts to heal with {character_data['items']['heal']['name']}!")

                            # Determine healing amount based on roll
                            healing = 0
                            if heal_total > 12:
                                healing = 3  # Major healing
                                action_log.append(f"MAJOR HEALING! Restores 3 HP!")
                            elif heal_total > 9:
                                healing = 2  # Moderate healing
                                action_log.append(f"Good healing! Restores 2 HP!")
                            elif heal_total > 7:
                                healing = 1  # Minor healing
                                action_log.append(f"Minor healing! Restores 1 HP!")
                            else:
                                action_log.append(f"Healing attempt fails!")

                            # Apply healing
                            old_player_health = player_health
                            player_health = min(5, player_health + healing)
                            character_data["health"] = player_health  # Update health in character_data
                            actual_healing = player_health - old_player_health

                            # Additional feedback if already at max health
                            if healing > 0 and actual_healing == 0:
                                action_log.append(f"{character_data['name']} is already at full health!")
                        else:
                            # No healing item
                            action_log.append(f"{character_data['name']} tries to heal but has no healing item!")

                    # Enemy's turn (if not defeated)
                    if enemy_health > 0:
                        # Enemy AI: If health is low (1-2), try to heal if possible
                        if enemy_health <= 2 and enemy_data['item_type'] == "HEAL":
                            # Roll for enemy healing effectiveness
                            enemy_heal_roll1, enemy_heal_roll2, enemy_heal_total = roll_dice(enemy_data['item_modifier'])

                            # Log the healing attempt
                            action_log.append(f"{enemy_data['name']} attempts to heal!")

                            # Determine healing amount based on roll
                            healing = 0
                            if enemy_heal_total > 12:
                                healing = 3  # Major healing
                                action_log.append(f"MAJOR HEALING! {enemy_data['name']} restores 3 HP!")
                            elif enemy_heal_total > 9:
                                healing = 2  # Moderate healing
                                action_log.append(f"Good healing! {enemy_data['name']} restores 2 HP!")
                            elif enemy_heal_total > 7:
                                healing = 1  # Minor healing
                                action_log.append(f"Minor healing! {enemy_data['name']} restores 1 HP!")
                            else:
                                action_log.append(f"{enemy_data['name']}'s healing attempt fails!")

                            # Apply healing
                            old_enemy_health = enemy_health
                            enemy_health = min(5, enemy_health + healing)
                            actual_healing = enemy_health - old_enemy_health

                            # Additional feedback if already at max health
                            if healing > 0 and actual_healing == 0:
                                action_log.append(f"{enemy_data['name']} is already at full health!")
                        else:
                            # Enemy attacks
                            # Get enemy's attack modifier
                            enemy_attack_mod = enemy_data['item_modifier'] if enemy_data['item_type'] == "ATTACK" else 0

                            # Get player's defense modifier
                            player_defense_mod = character_data['items'].get('defense',{}).get('modifier',0)

                            # Roll for attack and defense
                            enemy_roll1, enemy_roll2, enemy_attack = roll_dice(enemy_attack_mod)
                            player_roll1, player_roll2, player_defense = roll_dice(player_defense_mod)

                            # Log the attack attempt
                            action_log.append(f"{enemy_data['name']} attacks!")
                            
                            # Determine if attack is successful and calculate damage tier
                            if enemy_attack >= player_defense:
                                # Calculate margin of success
                                margin = enemy_attack - player_defense

                                # Determine damage based on margin
                                damage = 1  # Base damage
                                if margin >= 6:
                                    damage = 3  # Critical hit
                                    action_log.append(f"CRITICAL HIT! {character_data['name']} takes {damage} damage!")
                                elif margin >= 3:
                                    damage = 2  # Strong hit
                                    action_log.append(f"Strong hit! {character_data['name']} takes {damage} damage!")
                                else:
                                    action_log.append(f"Hit! {character_data['name']} takes {damage} damage!")

                                # Apply damage
                                player_health = max(0, player_health - damage)
                                character_data["health"] = player_health  # Update health in character_data

                                # Check if player is defeated
                                if player_health <= 0:
                                    action_log.append(f"{character_data['name']} has been defeated!")
                                    # Show game over screen
                                    if game_over_screen.game_over_screen(screen, character_data, enemy_defeated):
                                        # Return to level selection
                                        character_data['return_to_title'] = True
                                        return character_data
                                    else:
                                        running = False
                                        return False
                                elif player_health == 1:
                                    action_log.append(f"{character_data['name']} is critically wounded!")
                            else:
                                # Attack fails
                                action_log.append(f"Attack fails! {character_data['name']} dodges the attack!")

                    # Keep log at a reasonable size
                    if len(action_log) > 19:
                        action_log = action_log[-19:]

        # Create gradient background
        for y in range(HEIGHT):
            color_value = max(0, 50 - y // 10)
            pygame.draw.line(screen, (0, 0, color_value), (0, y), (WIDTH, y))

        # Add key controls to change health level (for demonstration)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            player_health = 1
        elif keys[pygame.K_2]:
            player_health = 2
        elif keys[pygame.K_3]:
            player_health = 3
        elif keys[pygame.K_4]:
            player_health = 4
        elif keys[pygame.K_5]:
            player_health = 5

        # Draw player and enemy cards
        draw_character_card(screen, character_data, player_card_x, player_card_y, card_width, card_height, player_health)
        draw_character_card(screen, enemy_data, enemy_card_x, enemy_card_y, card_width, card_height, enemy_health, True)

        # Draw game title (right-aligned, outside game area)
        # Title removed as requested

        # Draw game area (action log)
        pygame.draw.rect(screen, LIGHT_BLUE, (game_area_x, game_area_y, game_area_width, game_area_height), 3)


        # Shop hint removed as requestedAbove the buttons, aligned with labels

        # Draw action log title
        log_title_font = pygame.font.SysFont('Arial', 24, bold=True)
        log_title_text = log_title_font.render("Action Log", True, WHITE)
        log_title_rect = log_title_text.get_rect()
        log_title_rect.midtop = (WIDTH//2, game_area_y + 10)
        screen.blit(log_title_text, log_title_rect)

        # Draw action log entries
        log_font = pygame.font.SysFont('Arial', 18)
        for i, log_entry in enumerate(action_log):
            log_text = log_font.render(log_entry, True, WHITE)
            log_rect = log_text.get_rect()
            log_rect.center = (WIDTH//2, game_area_y + 50 + (i * 30))
            screen.blit(log_text, log_rect)

        # Draw action buttons
        attack_button.draw(screen)
        heal_button.draw(screen)
        run_button.draw(screen)

        # Draw action instructions
        instruction_font = pygame.font.SysFont('Arial', 18)
        instruction_text = instruction_font.render("Click an action button to perform that action", True, WHITE)
        screen.blit(instruction_text, (game_area_x, button_y - 30))

        pygame.display.flip()
        clock.tick(60)

    return character_data  # Return character data instead of False

# Dice roll function (2d6 + modifier)
def roll_dice(modifier=0):
    # Roll two six-sided dice
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    total = roll1 + roll2 + modifier
    return roll1, roll2, total