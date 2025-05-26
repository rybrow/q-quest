from src import loot_screen, title_screen, level_selection_screen, map_screen, combat_screen
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT
import pygame


# Initialize Pygame
pygame.init()
pygame.key.set_repeat(500, 50)  # Key repeat for text input

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Quest!")

def main(debug_mode=False):
    restart = True
    while restart:
        # Show title screen first
        title_screen.title_screen(screen)

        # Show character creation screen
        # Character creation removed - using level player data instead
        # Show level selection screen after title screen
        selected_level = level_selection_screen.level_selection_screen(screen)
        if not selected_level:
            continue  # Go back to title screen if no level selected

        # Use the player data from the selected level
        character_data = selected_level['player']

        # Add the level information to character_data
        character_data['level'] = {
            'id': selected_level['id'],
            'name': selected_level['name'],
            'path': selected_level['path'],
            'directory': selected_level['directory'],
            'starting_position': selected_level['starting_position'],
            'wall_tiles': selected_level['wall_tiles'],
            'enemies': selected_level['enemies'],
            'image': f"{selected_level['directory']}/{selected_level.get('player', {}).get('image', 'placeholder.png')}"
        }
        
        # Add debug mode flag to character data
        character_data['debug_mode'] = debug_mode

        # Show map screen after character creation
        if character_data:
            # Show map screen
            # Game flow control
            while True:

                # Explicit check for start_combat flag after map_screen
                if character_data.get('return_to_title', False):
                    print("Returning to level selection screen...")
                    break  # Break out of the game flow loop to return to level selection
                
                if character_data.get('start_combat', False):
                    print("Detected start_combat flag after map_screen, starting combat...")
                    enemy = character_data.get('current_enemy')
                    if enemy:
                        print(f"Starting combat with {enemy.get('name', 'Unknown')}")
                        character_data = combat_screen.main_game_screen(screen, character_data)
                        character_data['start_combat'] = False  # Reset the flag
                        # After combat, continue the loop to check for return_to_map
                        continue

                # Check if we need to show loot screen
                if character_data.get('show_loot', False):
                    # Show loot screen with stored enemy data
                    enemy_data = character_data.pop('loot_enemy')  # Get and remove stored enemy
                    character_data.pop('show_loot')  # Remove flag
                    character_data = loot_screen.loot_screen(screen, character_data, enemy_data)
                    # Continue to next iteration to check return_to_map flag
                    continue

                # Show map screen
                character_data = map_screen.map_screen(screen, character_data)
