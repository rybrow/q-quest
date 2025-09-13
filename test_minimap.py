#!/usr/bin/env python3

"""
Simple test script to verify the minimap functionality
"""

import sys
import os

# Add the workspace to the Python path
sys.path.insert(0, '/workspace')

try:
    # Test imports
    print("Testing imports...")
    from src.ui import draw_minimap
    from src.map_renderer import render_map_to_surface
    import pygame
    import pytmx
    
    print("✓ All imports successful")
    
    # Test pygame initialization
    print("Testing pygame initialization...")
    pygame.init()
    print("✓ Pygame initialized")
    
    # Test if we can load a sample map
    print("Testing map loading...")
    sample_map_path = "/workspace/levels/1_tower/maps/tower_map.tmx"
    if os.path.exists(sample_map_path):
        print(f"✓ Sample map file exists: {sample_map_path}")
        
        # Try to load the TMX data
        try:
            tmx_data = pytmx.load_pygame(sample_map_path)
            print(f"✓ TMX data loaded successfully")
            print(f"  Map size: {tmx_data.width}x{tmx_data.height}")
            print(f"  Tile size: {tmx_data.tilewidth}x{tmx_data.tileheight}")
        except Exception as e:
            print(f"✗ Error loading TMX data: {e}")
            
        # Try to render a minimap surface
        try:
            minimap_surface = render_map_to_surface(sample_map_path, 200, 200)
            print(f"✓ Minimap surface created successfully")
            print(f"  Surface size: {minimap_surface.get_size()}")
        except Exception as e:
            print(f"✗ Error creating minimap surface: {e}")
    else:
        print(f"✗ Sample map file not found: {sample_map_path}")
    
    print("\n=== Test Summary ===")
    print("Basic functionality test completed.")
    print("If no errors above, the minimap should work in the game.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)
finally:
    # Clean up pygame
    try:
        pygame.quit()
    except:
        pass