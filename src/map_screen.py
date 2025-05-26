import os
import random
import pygame
import sys

import pytmx
from src.map_config import MapConfig
from src.ui import WIDTH, HEIGHT, WHITE, BLACK, DARK_GRAY, BLUE, LIGHT_BLUE, GREEN, RED, YELLOW, GRAY, HIGHLIGHT, draw_character_card
from src.ui import calculate_card_height

# Main game screen function
def map_screen(screen, character_data):
    # Check if debug mode is enabled
    debug_mode = character_data.get('debug_mode', False)
    
    if debug_mode:
        print("\n==== MAP SCREEN ====")
        print(f"Character data type: {type(character_data)}")
        if isinstance(character_data, dict):
            print(f"Character data keys: {character_data.keys()}")
            if 'current_enemy' in character_data:
                print(f"Current enemy: {character_data['current_enemy']}")
            if 'level' in character_data:
                print(f"Level data keys: {character_data['level'].keys() if isinstance(character_data['level'], dict) else type(character_data['level'])}")
                if isinstance(character_data['level'], dict) and 'enemies' in character_data['level']:
                    print(f"Enemies in level: {character_data['level']['enemies']}")

    """
    Display the map screen with the player card and a rendered tilemap

    Args:
        character_data: Dictionary containing the player character data

    Returns:
        Updated character data
    """
    # Initialize variables
    running = True
    clock = pygame.time.Clock()


    # print(f"Character Data {json.dumps(character_data)}")

    # Screen dimensions
    WIDTH = 1280
    HEIGHT = 720

    # Margin for spacing
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
    card_height = calculate_card_height(item_y_start, item_height, item_spacing)

    # Player card position (left side, top of screen)
    player_card_x = margin
    player_card_y = margin

    # Initialize player health for display
    player_health = character_data.get('health', 5)

    # Map area position and dimensions
    map_area_x = card_width + (2 * margin)
    map_area_y = margin
    map_area_width = WIDTH - map_area_x - margin
    map_area_height = HEIGHT - (2 * margin)

    # Load map configuration
    map_config = None
    tmx_data = None

    # Check if we have level information in character_data
    if 'level' in character_data:
        level_info = character_data['level']
        map_path = os.path.join(level_info['directory'], level_info['path'])
        print(f"Map path: {map_path}")

        # Create a map config from the level info
        # Create a custom map configuration
        map_config = {
            "id": level_info['id'],
            "name": level_info['name'],
            "path": level_info['path'],
            "starting_position": level_info['starting_position'],
            "wall_tiles": level_info['wall_tiles'],
            "enemies": level_info['enemies']
        }


        try:
            tmx_data = pytmx.load_pygame(map_path)
            print(f"Loaded map from {map_path}")
        except Exception as e:
            print(f"Error loading map: {e}")
            # Fall back to default map
            map_config = None


    # Initialize player position
    # Check if returning from combat
    if character_data.get('return_to_map', False) and 'pre_combat_position' in character_data:
        # Restore position from before combat
        player_x, player_y = character_data['pre_combat_position']['x'], character_data['pre_combat_position']['y']
        print(f"Restoring position after combat: {player_x}, {player_y}")
        character_data['return_to_map'] = False
    else:
        # Use starting position from map config
        starting_position = map_config.get('starting_position', {}) if map_config else {}
        player_x = starting_position.get('x', 2)
        player_y = starting_position.get('y', 2)
    # Default player position if all else fails
    if 'player_x' not in locals() or 'player_y' not in locals():
            player_x, player_y = map_config.starting_position['x'], map_config.starting_position['y'] if map_config and hasattr(map_config, 'starting_position') else (0, 0)
    tile_width = 32
    tile_height = 32
    visible_tiles = 11
    zoom_factor = 1.0
    zoomed_tile_width = 32
    zoomed_tile_height = 32
    player_size = 32
    player_color = (0, 255, 0)  # Green

    # Log map loading
    print(f"Loading map: {map_config['name']} from {map_path}")
    print(f"Starting position: ({player_x}, {player_y})")

    try:
        # Load the TMX data
        tmx_data = pytmx.load_pygame(map_path)

        # Tile size (from the TMX file)
        tile_width = tmx_data.tilewidth
        tile_height = tmx_data.tileheight

        # Visible area (5 tiles on each side of the player)
        visible_tiles = 11  # Player + 5 on each side

        # Calculate the zoom factor to fit the visible area in the map display area
        zoom_factor = min(
            map_area_width / (visible_tiles * tile_width),
            map_area_height / (visible_tiles * tile_height)
        )

        # Size of tiles after zooming
        zoomed_tile_width = tile_width * zoom_factor
        zoomed_tile_height = tile_height * zoom_factor

        # Player size and color
        player_size = min(zoomed_tile_width, zoomed_tile_height)
        player_color = (0, 255, 0)  # Green

        # Movement cooldown to control speed
        move_cooldown = 0
        cooldown_time = 150  # milliseconds

    except Exception as e:
        print(f"Error loading map: {e}")
        tmx_data = None

    # Continue button removed

    # Main loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Exit the game when Escape is pressed
            # Continue button handling removed

        # Handle player movement with WASD
        if tmx_data and move_cooldown <= 0:
            keys = pygame.key.get_pressed()
            moved = False

            # Get wall tiles from config
            wall_tiles = map_config['wall_tiles']

            # Store current position for reverting if needed
            new_x, new_y = player_x, player_y

            # Check movement in each direction - one direction at a time, no diagonal movement
            # Only process one key at a time in priority order: up, down, left, right
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if character_data.get('debug_mode', False):
                    print("K_UP")
                if player_y > 0:
                    new_y = player_y - 1
                    moved = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if character_data.get('debug_mode', False):
                    print("K_DOWN")
                if player_y < tmx_data.height - 1:
                    new_y = player_y + 1
                    moved = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if character_data.get('debug_mode', False):
                    print("K_LEFT")
                if player_x > 0:
                    new_x = player_x - 1
                    moved = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if character_data.get('debug_mode', False):
                    print("K_RIGHT")
                if player_x < tmx_data.width - 1:
                    new_x = player_x + 1
                    moved = True
                # if player_x < tmx_data.width - 1:
                #     new_x = player_x + 1
                #     moved = True

            # Only update position if the new position is walkable
            if moved:
                if character_data.get('debug_mode', False):
                    print(f"Attempting to move to ({new_x}, {new_y})")
                walkable = is_walkable(new_x, new_y, tmx_data, wall_tiles, character_data.get('debug_mode', False))
                if character_data.get('debug_mode', False):
                    print(f"Position is walkable: {walkable}")

                if walkable:
                    print("\n==== CHECKING FOR ENEMY COLLISION ====")
                    if character_data.get('debug_mode', False):
                        print(f"Checking position: ({new_x}, {new_y})")
                        if 'level' in character_data and 'enemies' in character_data['level']:
                            print(f"Available enemies: {character_data['level']['enemies']}")
                            for e in character_data['level']['enemies']:
                                if 'position' in e:
                                    print(f"Enemy {e.get('name', 'Unknown')} at position {e['position'].get('x')}, {e['position'].get('y')}")

                    # Check for enemy collision
                    enemy = None

                    # Only check enemies from level data
                    if 'level' in character_data and 'enemies' in character_data['level']:
                        for e in character_data['level']['enemies']:
                            if 'position' in e and e['position'].get('x') == new_x and e['position'].get('y') == new_y:
                                enemy = e
                                print(f"Found enemy in level data: {e.get('name')}")
                                break

                    if enemy:
                        if character_data.get('debug_mode', False):
                            print(f"Collided with enemy: {enemy.get('name', 'Unknown')}")
                        # Store the enemy data for combat
                        character_data['current_enemy'] = enemy

                        # Store the player's position before combat
                        character_data['pre_combat_position'] = {'x': player_x, 'y': player_y}
                        if character_data.get('debug_mode', False):
                            print(f"Storing pre-combat position: {player_x}, {player_y}")

                        # Set flag to exit map screen and start combat
                        character_data['start_combat'] = True
                        if character_data.get('debug_mode', False):
                            print(f"Setting start_combat flag to True")
                        running = False
                        return character_data  # Return immediately to ensure flag is processed
                    else:
                        # No enemy, just move
                        if character_data.get('debug_mode', False):
                            print(f"Moving to ({new_x}, {new_y})")
                        player_x, player_y = new_x, new_y
                        move_cooldown = cooldown_time
                else:
                    # Play a sound or visual effect to indicate collision
                    # For now, just set a shorter cooldown
                    if character_data.get('debug_mode', False):
                        print(f"Cannot move to ({new_x}, {new_y}) - collision detected")
                    move_cooldown = cooldown_time // 2

        # Update cooldown
        if move_cooldown > 0:
            move_cooldown -= clock.get_time()

        # Clear the screen
        screen.fill(BLACK)

        # Draw background gradient
        for y in range(HEIGHT):
            color_value = max(0, 50 - y // 10)
            pygame.draw.line(screen, (0, 0, color_value), (0, y), (WIDTH, y))

        # Draw player card
        draw_character_card(screen, character_data, player_card_x, player_card_y, card_width, card_height, player_health)

        # Create a surface for the map area
        map_surface = pygame.Surface((map_area_width, map_area_height))
        map_surface.fill((20, 20, 40))  # Dark blue background

        if tmx_data:
            try:
                # Calculate the center of the map area in pixels
                center_x = map_area_width / 2
                center_y = map_area_height / 2

                # Calculate the offset to center the view on the player
                offset_x = center_x - (player_x * zoomed_tile_width) - (zoomed_tile_width / 2)
                offset_y = center_y - (player_y * zoomed_tile_height) - (zoomed_tile_height / 2)

                # Draw the visible portion of the map
                for layer in tmx_data.visible_layers:
                    if hasattr(layer, 'data'):
                        for x in range(max(0, player_x - 6), min(tmx_data.width, player_x + 7)):
                            for y in range(max(0, player_y - 6), min(tmx_data.height, player_y + 7)):
                                # Get the tile image
                                gid = layer.data[y][x]
                                if gid:
                                    tile = tmx_data.get_tile_image_by_gid(gid)
                                    if tile:
                                        # Scale the tile
                                        scaled_tile = pygame.transform.scale(
                                            tile,
                                            (int(zoomed_tile_width), int(zoomed_tile_height))
                                        )

                                        # Calculate position with offset
                                        pos_x = int(x * zoomed_tile_width + offset_x)
                                        pos_y = int(y * zoomed_tile_height + offset_y)

                                        # Draw the tile
                                        map_surface.blit(scaled_tile, (pos_x, pos_y))

                # Draw enemies
                # Only use enemies from level data
                enemies = []

                # Add enemies from level data if available
                if 'level' in character_data and 'enemies' in character_data['level']:
                    enemies = character_data['level']['enemies']

                for enemy in enemies:
                    if 'position' in enemy:
                        enemy_x = enemy['position'].get('x', 0)
                        enemy_y = enemy['position'].get('y', 0)

                        # Calculate position with offset
                        pos_x = int(enemy_x * zoomed_tile_width + offset_x)
                        pos_y = int(enemy_y * zoomed_tile_height + offset_y)

                        # Only draw if in visible area
                        if (pos_x + zoomed_tile_width > 0 and pos_x < map_area_width and
                            pos_y + zoomed_tile_height > 0 and pos_y < map_area_height):

                            # Draw enemy using image if available, otherwise use red box
                            enemy_size = player_size
                            enemy_rect = pygame.Rect(
                                pos_x + (zoomed_tile_width - enemy_size) / 2,
                                pos_y + (zoomed_tile_height - enemy_size) / 2,
                                enemy_size,
                                enemy_size
                            )
                            
                            # Try to load and use enemy icon if available, otherwise fall back to image
                            enemy_icon_path = None
                            enemy_image_path = None
                            
                            # First try to use icon
                            if 'icon' in enemy:
                                enemy_icon_path = os.path.join(character_data['level']['directory'], enemy['icon'])
                            
                            # Then try to use image as fallback
                            if 'image' in enemy:
                                enemy_image_path = os.path.join(character_data['level']['directory'], enemy['image'])
                            
                            # Try icon first
                            if enemy_icon_path and os.path.exists(enemy_icon_path):
                                try:
                                    enemy_image = pygame.image.load(enemy_icon_path)
                                    enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
                                    map_surface.blit(enemy_image, enemy_rect)
                                except Exception as e:
                                    print(f"Error loading enemy icon {enemy_icon_path}: {e}")
                                    # Fall back to portrait image if icon fails
                                    if enemy_image_path and os.path.exists(enemy_image_path):
                                        try:
                                            enemy_image = pygame.image.load(enemy_image_path)
                                            enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
                                            map_surface.blit(enemy_image, enemy_rect)
                                        except Exception as e:
                                            print(f"Error loading enemy image {enemy_image_path}: {e}")
                                            pygame.draw.rect(map_surface, (255, 0, 0), enemy_rect)  # Red fallback
                                            pygame.draw.rect(map_surface, (255, 255, 255), enemy_rect, 2)  # White border
                                    else:
                                        pygame.draw.rect(map_surface, (255, 0, 0), enemy_rect)  # Red fallback
                                        pygame.draw.rect(map_surface, (255, 255, 255), enemy_rect, 2)  # White border
                            # Try portrait image if no icon
                            elif enemy_image_path and os.path.exists(enemy_image_path):
                                try:
                                    enemy_image = pygame.image.load(enemy_image_path)
                                    enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
                                    map_surface.blit(enemy_image, enemy_rect)
                                except Exception as e:
                                    print(f"Error loading enemy image {enemy_image_path}: {e}")
                                    pygame.draw.rect(map_surface, (255, 0, 0), enemy_rect)  # Red fallback
                                    pygame.draw.rect(map_surface, (255, 255, 255), enemy_rect, 2)  # White border
                            else:
                                # Fallback to red box if no images available
                                pygame.draw.rect(map_surface, (255, 0, 0), enemy_rect)  # Red for enemies
                                pygame.draw.rect(map_surface, (255, 255, 255), enemy_rect, 2)  # White border

                # Draw the player using image if available, otherwise use green box
                player_rect = pygame.Rect(
                    center_x - (player_size / 2),
                    center_y - (player_size / 2),
                    player_size,
                    player_size
                )
                
                # Try to load and use player icon if available, otherwise fall back to image
                player_icon_path = None
                player_image_path = None
                
                # First try to use icon
                if 'icon' in character_data:
                    player_icon_path = os.path.join(character_data['level']['directory'], character_data['icon'])
                
                # Then try to use image as fallback
                if 'image' in character_data:
                    player_image_path = os.path.join(character_data['level']['directory'], character_data['image'])
                
                # Try icon first
                if player_icon_path and os.path.exists(player_icon_path):
                    try:
                        player_image = pygame.image.load(player_icon_path)
                        player_image = pygame.transform.scale(player_image, (player_size, player_size))
                        map_surface.blit(player_image, player_rect)
                    except Exception as e:
                        print(f"Error loading player icon {player_icon_path}: {e}")
                        # Fall back to portrait image if icon fails
                        if player_image_path and os.path.exists(player_image_path):
                            try:
                                player_image = pygame.image.load(player_image_path)
                                player_image = pygame.transform.scale(player_image, (player_size, player_size))
                                map_surface.blit(player_image, player_rect)
                            except Exception as e:
                                print(f"Error loading player image {player_image_path}: {e}")
                                pygame.draw.rect(map_surface, player_color, player_rect)  # Green fallback
                                pygame.draw.rect(map_surface, (255, 255, 255), player_rect, 2)  # White border
                        else:
                            pygame.draw.rect(map_surface, player_color, player_rect)  # Green fallback
                            pygame.draw.rect(map_surface, (255, 255, 255), player_rect, 2)  # White border
                # Try portrait image if no icon
                elif player_image_path and os.path.exists(player_image_path):
                    try:
                        player_image = pygame.image.load(player_image_path)
                        player_image = pygame.transform.scale(player_image, (player_size, player_size))
                        map_surface.blit(player_image, player_rect)
                    except Exception as e:
                        print(f"Error loading player image {player_image_path}: {e}")
                        pygame.draw.rect(map_surface, player_color, player_rect)  # Green fallback
                        pygame.draw.rect(map_surface, (255, 255, 255), player_rect, 2)  # White border
                else:
                    # Fallback to green box if no images available
                    pygame.draw.rect(map_surface, player_color, player_rect)
                    pygame.draw.rect(map_surface, (255, 255, 255), player_rect, 2)  # White border

            except Exception as e:
                print(f"Error rendering map: {e}")
                font = pygame.font.SysFont('Arial', 24)
                error_text = font.render(f"Error rendering map: {e}", True, (255, 0, 0))
                map_surface.blit(error_text, (20, 20))
        else:
            # Draw error message if map couldn't be loaded
            font = pygame.font.SysFont('Arial', 24)
            error_text = font.render("Error loading map", True, (255, 0, 0))
            map_surface.blit(error_text, (20, 20))

        # Draw the map surface
        screen.blit(map_surface, (map_area_x, map_area_y))

        # Draw map border
        pygame.draw.rect(screen, (100, 100, 150), (map_area_x, map_area_y, map_area_width, map_area_height), 2)

        # Map title removed

        # Draw instructions
        instruction_font = pygame.font.SysFont('Arial', 18)
        # Instruction label removed as requested

        # Continue button drawing removed

        # Draw player coordinates and debug info
        if tmx_data and character_data.get('debug_mode', False):
            coord_font = pygame.font.SysFont('Arial', 16)
            coord_text = coord_font.render(f"Position: ({player_x}, {player_y})", True, (200, 200, 200))
            screen.blit(coord_text, (map_area_x + 10, map_area_y + 10))

            # Draw wall tile info
            wall_tiles = map_config['wall_tiles']
            wall_text = coord_font.render(f"Wall tiles: {wall_tiles[:5]}{'...' if len(wall_tiles) > 5 else ''}", True, (200, 200, 200))
            screen.blit(wall_text, (map_area_x + 10, map_area_y + 30))

            # Get current tile info
            current_tile_info = "Current tile: "
            for layer in tmx_data.visible_layers:
                if hasattr(layer, 'data'):
                    tile_gid = layer.data[player_y][player_x]
                    current_tile_info += f"GID={tile_gid} "

                    # Convert GID to tile ID
                    if tile_gid > 0:
                        for tileset in tmx_data.tilesets:
                            if tile_gid >= tileset.firstgid and tile_gid < tileset.firstgid + tileset.tilecount:
                                tile_id = tile_gid - tileset.firstgid + 1
                                current_tile_info += f"(ID={tile_id})"

            tile_text = coord_font.render(current_tile_info, True, (200, 200, 200))
            screen.blit(tile_text, (map_area_x + 10, map_area_y + 50))

            # Draw enemy count
            enemies = []

            # Only use enemies from level data
            if 'level' in character_data and 'enemies' in character_data['level']:
                enemies = character_data['level']['enemies']

            enemy_text = coord_font.render(f"Enemies: {len(enemies)}", True, (200, 200, 200))
            screen.blit(enemy_text, (map_area_x + 10, map_area_y + 70))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    # Store player position and map data in character data for future use
    if tmx_data:
        # Store position
        character_data['map_position'] = (player_x, player_y)

        # Store current map ID
        character_data['current_map'] = map_config['id']

    return character_data


# Function to check if a position is walkable
def is_walkable(x, y, tmx_data, wall_tiles, debug_mode=False):
    # Check map boundaries
    if x < 0 or y < 0 or x >= tmx_data.width or y >= tmx_data.height:
        if debug_mode:
            print(f"Position ({x}, {y}) is out of bounds")
        return False

    # Check for wall tiles in all layers
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            tile_gid = layer.data[y][x]

            # Special case: if GID is 0 (empty tile) and 0 is in wall_tiles
            if tile_gid == 0 and 0 in wall_tiles:
                if character_data.get('debug_mode', False):
                    print(f"Position ({x}, {y}) has GID 0 (empty tile) which is a wall")
                return False

            # For non-zero GIDs, convert to tile ID
            if tile_gid > 0:
                # Convert GID to tile ID by subtracting firstgid
                for tileset in tmx_data.tilesets:
                    if tile_gid >= tileset.firstgid and tile_gid < tileset.firstgid + tileset.tilecount:
                        tile_id = tile_gid - tileset.firstgid + 1  # +1 because TMX tile IDs start at 1
                        if tile_id in wall_tiles:
                            if character_data.get('debug_mode', False):
                                print(f"Position ({x}, {y}) has tile ID {tile_id} which is a wall")
                            return False

    return True
