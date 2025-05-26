import os
import json

class MapConfig:
    """
    Class to handle loading and managing map configurations from a JSON file
    """
    def __init__(self, config_path="config/maps.json"):
        """
        Initialize the MapConfig with a path to the configuration file

        Args:
            config_path: Path to the JSON configuration file
        """
        self.config_path = config_path
        self.maps = {}
        self.default_map = None
        self.load_config()

    def load_config(self):
        """
        Load the map configuration from the JSON file
        """
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            # Load maps from config
            for map_data in config.get('maps', []):
                map_id = map_data.get('id')
                if map_id:
                    self.maps[map_id] = map_data

            # Set default map
            self.default_map = config.get('default_map')

            print(f"Loaded {len(self.maps)} maps from configuration")

        except Exception as e:
            print(f"Error loading map configuration: {e}")
            raise e

    def get_map(self, map_id=None):
        """
        Get a map configuration by ID

        Args:
            map_id: ID of the map to get, or None to get the default map

        Returns:
            Map configuration dictionary, or None if not found
        """
        if map_id is None:
            map_id = self.default_map

        return self.maps.get(map_id)

    def get_map_path(self, map_id=None):
        """
        Get the file path for a map

        Args:
            map_id: ID of the map to get the path for, or None to get the default map

        Returns:
            Path to the map file, or None if not found
        """
        map_config = self.get_map(map_id)
        if map_config:
            return map_config.get('path')
        return None

    def get_starting_position(self, map_id=None):
        """
        Get the starting position for a map

        Args:
            map_id: ID of the map to get the starting position for, or None to get the default map

        Returns:
            Tuple of (x, y) coordinates, or (5, 5) if not found
        """
        map_config = self.get_map(map_id)
        if map_config and 'starting_position' in map_config:
            pos = map_config['starting_position']
            return (pos.get('x', 5), pos.get('y', 5))
        return (5, 5)

    def get_wall_tiles(self, map_id=None):
        """
        Get the list of tile IDs that represent walls for a map

        Args:
            map_id: ID of the map to get wall tiles for, or None to get the default map

        Returns:
            List of tile IDs that represent walls, or [0] if not found
        """
        map_config = self.get_map(map_id)
        if map_config and 'wall_tiles' in map_config:
            return map_config['wall_tiles']
        return [0]  # Default: treat tile ID 0 as a wall

    def is_wall_tile(self, tile_id, map_id=None):
        """
        Check if a tile ID represents a wall

        Args:
            tile_id: The tile ID to check
            map_id: ID of the map to check against, or None to use the default map

        Returns:
            True if the tile ID represents a wall, False otherwise
        """
        wall_tiles = self.get_wall_tiles(map_id)
        return tile_id in wall_tiles

    def get_enemies(self, map_id=None):
        """
        Get the list of enemies for a map

        Args:
            map_id: ID of the map to get enemies for, or None to get the default map

        Returns:
            List of enemy dictionaries, or [] if not found
        """
        map_config = self.get_map(map_id)
        if map_config and 'enemies' in map_config:
            return map_config['enemies']
        return []  # Default: no enemies

    def get_enemy_at_position(self, x, y, map_id=None):
        """
        Get an enemy at the specified position

        Args:
            x: X coordinate
            y: Y coordinate
            map_id: ID of the map to check, or None to use the default map

        Returns:
            Enemy dictionary if found, None otherwise
        """
        enemies = self.get_enemies(map_id)
        for enemy in enemies:
            if 'position' in enemy:
                pos = enemy['position']
                if pos.get('x') == x and pos.get('y') == y:
                    return enemy
        return None

    def get_all_maps(self):
        """
        Get all available maps

        Returns:
            List of map configuration dictionaries
        """
        return list(self.maps.values())
