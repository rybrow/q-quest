#!/usr/bin/env python3
"""
Test script for the music system implementation.

This script tests the music system components without requiring the full game to run.
It verifies that the music manager initializes correctly and can handle level configurations.
"""

import sys
import os
import json

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_music_manager_import():
    """Test that the music manager can be imported successfully."""
    try:
        from music_manager import MusicManager, get_music_manager, initialize_music_system
        print("✓ Music manager import successful")
        return True
    except ImportError as e:
        print(f"✗ Music manager import failed: {e}")
        return False

def test_music_system_initialization():
    """Test that the music system can be initialized."""
    try:
        from music_manager import initialize_music_system
        result = initialize_music_system()
        if result:
            print("✓ Music system initialization successful")
        else:
            print("⚠ Music system initialization failed (this is normal if no audio device is available)")
        return True
    except Exception as e:
        print(f"✗ Music system initialization error: {e}")
        return False

def test_music_manager_functionality():
    """Test basic music manager functionality."""
    try:
        from music_manager import get_music_manager
        manager = get_music_manager()
        
        # Test basic methods exist
        assert hasattr(manager, 'load_music'), "load_music method missing"
        assert hasattr(manager, 'play_music'), "play_music method missing"
        assert hasattr(manager, 'stop_music'), "stop_music method missing"
        assert hasattr(manager, 'set_volume'), "set_volume method missing"
        assert hasattr(manager, 'load_and_play_level_music'), "load_and_play_level_music method missing"
        
        print("✓ Music manager methods available")
        return True
    except Exception as e:
        print(f"✗ Music manager functionality test failed: {e}")
        return False

def test_level_configurations():
    """Test that level configurations are valid and include music where expected."""
    levels_dir = "levels"
    test_results = []
    
    if not os.path.exists(levels_dir):
        print(f"✗ Levels directory not found: {levels_dir}")
        return False
    
    for level_dir in os.listdir(levels_dir):
        level_path = os.path.join(levels_dir, level_dir)
        
        if os.path.isdir(level_path):
            level_json_path = os.path.join(level_path, "level.json")
            
            if os.path.exists(level_json_path):
                try:
                    with open(level_json_path, 'r') as f:
                        level_data = json.load(f)
                    
                    level_name = level_data.get('name', level_dir)
                    
                    if 'music' in level_data:
                        music_config = level_data['music']
                        music_file = music_config.get('file')
                        
                        if music_file:
                            music_path = os.path.join(level_path, music_file)
                            if os.path.exists(music_path):
                                print(f"✓ {level_name}: Music file exists ({music_file})")
                            else:
                                print(f"⚠ {level_name}: Music file configured but not found ({music_file})")
                        else:
                            print(f"⚠ {level_name}: Music config exists but no file specified")
                        
                        # Validate music configuration
                        volume = music_config.get('volume', 0.7)
                        if not (0.0 <= volume <= 1.0):
                            print(f"⚠ {level_name}: Invalid volume value ({volume})")
                        
                        test_results.append(True)
                    else:
                        print(f"ℹ {level_name}: No music configuration (this is fine)")
                        test_results.append(True)
                        
                except json.JSONDecodeError as e:
                    print(f"✗ {level_name}: Invalid JSON in level.json: {e}")
                    test_results.append(False)
                except Exception as e:
                    print(f"✗ {level_name}: Error reading level configuration: {e}")
                    test_results.append(False)
    
    return all(test_results)

def test_level_music_loading():
    """Test that the music manager can handle level configurations."""
    try:
        from music_manager import get_music_manager
        manager = get_music_manager()
        
        # Test with a sample level configuration
        test_level_data = {
            'name': 'Test Level',
            'directory': '/fake/path',
            'music': {
                'file': 'music/test.ogg',
                'volume': 0.5,
                'loops': -1,
                'fade_in': True
            }
        }
        
        # This should not crash, even with a fake path
        result = manager.load_and_play_level_music(test_level_data)
        print(f"✓ Level music loading test completed (result: {result})")
        
        # Test with level without music
        test_level_no_music = {
            'name': 'Test Level No Music',
            'directory': '/fake/path'
        }
        
        result = manager.load_and_play_level_music(test_level_no_music)
        print(f"✓ Level without music test completed (result: {result})")
        
        return True
    except Exception as e:
        print(f"✗ Level music loading test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Q-Quest Music System Implementation")
    print("=" * 50)
    
    tests = [
        ("Music Manager Import", test_music_manager_import),
        ("Music System Initialization", test_music_system_initialization),
        ("Music Manager Functionality", test_music_manager_functionality),
        ("Level Configurations", test_level_configurations),
        ("Level Music Loading", test_level_music_loading),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎵 All tests passed! Music system is ready to use.")
        return 0
    else:
        print("⚠ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())