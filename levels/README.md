# Levels System

This directory contains the levels for the Q-Quest! game.

## Structure

Each level is contained in its own directory with the following structure:

```
level1/
  ├── level.json       # Level definition
  └── assets/
      ├── maps/        # Map files (.tmx)
      └── images/      # Images for the level
```

## Level Definition

The `level.json` file defines the level with the following structure:

```json
{
  "id": "unique_id",
  "name": "Display Name",
  "description": "Level description",
  "difficulty": "Easy|Medium|Hard|Expert",
  "path": "assets/maps/map_file.tmx",
  "starting_position": {
    "x": 5,
    "y": 5
  },
  "wall_tiles": [0, 23, 45],
  "player": {
    "name": "Player Name",
    "image": "assets/images/player.png",
    "health": 5,
    "items": {
      "attack": {
        "name": "Weapon Name",
        "modifier": 1
      },
      "defense": {
        "name": "Armor Name",
        "modifier": 1
      },
      "heal": {
        "name": "Potion Name",
        "modifier": 1
      }
    },
    "currency": 50,
    "description": "Player description"
  },
  "enemies": [
    {
      "name": "Enemy Name",
      "image": "assets/images/enemy.png",
      "health": 3,
      "items": {
        "attack": {
          "name": "Weapon Name",
          "modifier": 1
        }
      },
      "position": {
        "x": 10,
        "y": 8
      },
      "currency": 15,
      "description": "Enemy description"
    }
  ]
}
```

## Playing a Level

To play a level, run:

```
python scripts/play_level.py
```

This will show the title screen, then character creation, then level selection.
