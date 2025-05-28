# Q-Quest!

A turn-based RPG adventure game made with the Amazon Q CLI, Assets powered by Bedrock and Amazon Nova.

## Installing Dependencies

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Run the Game
python3 run_game.py
```

## Game Structure and Flow

### Entry Point
- `run_game.py`: The main entry point that initializes the game and handles exceptions

### Core Components

1. **Main Game Loop** (`src/main.py`)
   - Controls the overall game flow
   - Manages transitions between different screens
   - Handles game state flags (combat, loot, return to map)

2. **UI Components** (`src/ui.py`)
   - Contains shared UI elements and constants
   - Defines colors, screen dimensions
   - Includes the Button class and character card drawing functions

3. **Title Screen** (`src/title_screen.py`)
   - First screen displayed when the game starts
   - Simple menu with options to start or quit

4. **Level Selection** (`src/level_selection_screen.py`)
   - Allows player to choose a level to play
   - Loads available levels from the levels directory

5. **Map Screen** (`src/map_screen.py`)
   - Displays the game map where the player can navigate
   - Handles player movement and collision detection
   - Triggers combat when player encounters enemies

6. **Combat Screen** (`src/combat_screen.py`)
   - Manages turn-based combat between player and enemies
   - Handles attack, defense, and healing actions
   - Updates player and enemy health

7. **Loot Screen** (`src/loot_screen.py`)
   - Displayed after defeating an enemy
   - Allows player to collect items from defeated enemies

8. **Game Over Screen** (`src/game_over_screen.py`)
   - Shown when player is defeated
   - Provides options to restart or quit

### Map Handling

1. **Map Configuration** (`src/map_config.py`)
   - Loads and manages map configurations from JSON files
   - Provides methods to access map properties

2. **Map Renderer** (`src/map_renderer.py`)
   - Renders TMX (Tiled Map Editor) maps
   - Handles tile-based map visualization

## Game Flow

1. **Start**: The game begins at the title screen
2. **Level Selection**: Player selects a level to play
3. **Map Navigation**: Player explores the map using arrow keys or WASD
4. **Combat**: When player collides with an enemy, combat begins
   - Player can attack, heal, or run
   - Combat continues until player or enemy is defeated
5. **Loot**: After defeating an enemy, player can collect loot
6. **Return to Map**: After combat or looting, player returns to the map
7. **Game Over**: If player's health reaches zero, game over screen is shown

## Key Game Mechanics

1. **Movement**: Arrow keys or WASD to navigate the map
2. **Combat**: Turn-based system with attack and defense rolls
3. **Items**: Players can collect and use different items for attack, defense, and healing
4. **Health**: Both player and enemies have health points
5. **Currency**: Gold can be collected from defeated enemies

## File Structure

- `run_game.py`: Entry point
- `src/`: Source code directory
  - `main.py`: Main game loop
  - `ui.py`: UI components and utilities
  - `title_screen.py`: Title screen implementation
  - `level_selection_screen.py`: Level selection screen
  - `map_screen.py`: Map navigation screen
  - `combat_screen.py`: Combat mechanics
  - `loot_screen.py`: Loot collection screen
  - `game_over_screen.py`: Game over screen
  - `map_config.py`: Map configuration handling
  - `map_renderer.py`: TMX map rendering
- `levels/`: Directory containing level data
  - Each level has its own subdirectory with:
    - `level.json`: Level configuration
    - `map.tmx`: Tiled map file (optional)
    - `placeholder.png`: Default image for characters

## Controls

- **Title Screen**: SPACE to start, ESC to quit
- **Level Selection**: Click on a level to select
- **Map Screen**: Arrow keys or WASD to move, ESC to exit
- **Combat Screen**: Click on action buttons (Attack, Heal, Run)
- **Loot Screen**: Click on items to collect, Skip to continue
