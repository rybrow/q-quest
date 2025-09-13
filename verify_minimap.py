#!/usr/bin/env python3

"""
Verification script for minimap implementation
This script checks that all the necessary components are in place
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (NOT FOUND)")
        return False

def check_function_in_file(filepath, function_name, description):
    """Check if a function exists in a file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if f"def {function_name}" in content:
                print(f"✓ {description}: {function_name} found in {filepath}")
                return True
            else:
                print(f"✗ {description}: {function_name} NOT found in {filepath}")
                return False
    except Exception as e:
        print(f"✗ Error checking {filepath}: {e}")
        return False

def check_import_in_file(filepath, import_statement, description):
    """Check if an import statement exists in a file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if import_statement in content:
                print(f"✓ {description}: Import found in {filepath}")
                return True
            else:
                print(f"✗ {description}: Import NOT found in {filepath}")
                return False
    except Exception as e:
        print(f"✗ Error checking {filepath}: {e}")
        return False

def main():
    print("=== Minimap Implementation Verification ===\n")
    
    all_checks_passed = True
    
    # Check core files exist
    print("1. Checking core files...")
    files_to_check = [
        ("/workspace/src/ui.py", "UI module"),
        ("/workspace/src/map_screen.py", "Map screen module"),
        ("/workspace/src/map_renderer.py", "Map renderer module"),
        ("/workspace/levels/1_tower/maps/tower_map.tmx", "Sample TMX map"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print("\n2. Checking function implementations...")
    
    # Check if draw_minimap function exists in ui.py
    if not check_function_in_file("/workspace/src/ui.py", "draw_minimap", "Minimap function"):
        all_checks_passed = False
    
    # Check if render_map_to_surface function exists in map_renderer.py
    if not check_function_in_file("/workspace/src/map_renderer.py", "render_map_to_surface", "Map renderer function"):
        all_checks_passed = False
    
    print("\n3. Checking imports...")
    
    # Check if draw_minimap is imported in map_screen.py
    if not check_import_in_file("/workspace/src/map_screen.py", "draw_minimap", "Minimap import"):
        all_checks_passed = False
    
    print("\n4. Checking minimap integration...")
    
    # Check if minimap is called in map_screen.py
    try:
        with open("/workspace/src/map_screen.py", 'r') as f:
            content = f.read()
            if "draw_minimap(screen, character_data, player_x, player_y, tmx_data, map_path)" in content:
                print("✓ Minimap integration: Function call found in map_screen.py")
            else:
                print("✗ Minimap integration: Function call NOT found in map_screen.py")
                all_checks_passed = False
    except Exception as e:
        print(f"✗ Error checking minimap integration: {e}")
        all_checks_passed = False
    
    print("\n5. Checking combat state detection...")
    
    # Check if combat state detection is implemented
    try:
        with open("/workspace/src/map_screen.py", 'r') as f:
            content = f.read()
            if "not character_data.get('start_combat', False)" in content:
                print("✓ Combat state detection: Found in map_screen.py")
            else:
                print("✗ Combat state detection: NOT found in map_screen.py")
                all_checks_passed = False
    except Exception as e:
        print(f"✗ Error checking combat state detection: {e}")
        all_checks_passed = False
    
    print("\n=== Verification Summary ===")
    if all_checks_passed:
        print("✓ All checks passed! Minimap implementation appears to be complete.")
        print("\nTo test the minimap:")
        print("1. Run: python3 run_game.py")
        print("2. Select a level")
        print("3. Look for the minimap in the bottom right corner")
        print("4. Move around to see the green dot (player) update")
        print("5. Approach enemies (red dots) to test combat state detection")
    else:
        print("✗ Some checks failed. Please review the implementation.")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())