import os
import pygame
import pytmx

class TiledMapRenderer:
    def __init__(self, filename):
        """
        Initialize the TiledMapRenderer with a TMX file
        
        Args:
            filename: Path to the TMX file
        """
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.tmx_data.filename = filename
        
    def render(self, surface):
        """
        Render the map to the given surface
        
        Args:
            surface: Pygame surface to render the map onto
        """
        # Fill with black in case some tiles are empty
        surface.fill((0, 0, 0))
        
        # Iterate through all visible layers
        for layer in self.tmx_data.visible_layers:
            # Check if this layer contains tiles
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    # Get the tile image
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Calculate the position to draw the tile
                        pos_x = x * self.tmx_data.tilewidth
                        pos_y = y * self.tmx_data.tileheight
                        # Draw the tile
                        surface.blit(tile, (pos_x, pos_y))
    
    def make_map_surface(self):
        """
        Create a surface with the entire map rendered on it
        
        Returns:
            A pygame Surface with the map rendered on it
        """
        # Create a surface the size of the map
        map_surface = pygame.Surface((self.width, self.height))
        self.render(map_surface)
        return map_surface

def render_map_to_surface(map_path, width, height):
    """
    Render a TMX map to a surface of the specified size
    
    Args:
        map_path: Path to the TMX file
        width: Width of the output surface
        height: Height of the output surface
        
    Returns:
        A pygame Surface with the map rendered on it, scaled to fit the specified dimensions
    """
    # Load and render the map
    map_renderer = TiledMapRenderer(map_path)
    map_surface = map_renderer.make_map_surface()
    
    # Scale the map to fit the specified dimensions
    # We'll preserve aspect ratio and center the map
    map_aspect = map_surface.get_width() / map_surface.get_height()
    target_aspect = width / height
    
    if map_aspect > target_aspect:
        # Map is wider than target area
        scale_factor = width / map_surface.get_width()
    else:
        # Map is taller than target area
        scale_factor = height / map_surface.get_height()
    
    # Scale the map
    scaled_width = int(map_surface.get_width() * scale_factor)
    scaled_height = int(map_surface.get_height() * scale_factor)
    scaled_map = pygame.transform.scale(map_surface, (scaled_width, scaled_height))
    
    # Create the final surface
    final_surface = pygame.Surface((width, height))
    final_surface.fill((0, 0, 0))
    
    # Center the map on the surface
    x_offset = (width - scaled_width) // 2
    y_offset = (height - scaled_height) // 2
    final_surface.blit(scaled_map, (x_offset, y_offset))
    
    return final_surface
