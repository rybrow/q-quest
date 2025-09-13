# Music Configuration for Wizard's Tower

This level is configured to play background music when loaded.

## Music File Configuration

The level.json file contains a music configuration that references:
- **File**: `music/tower_theme.ogg`
- **Volume**: 60% (0.6)
- **Loops**: Infinite (-1)
- **Fade In**: Enabled

## Adding Music Files

To add actual music to this level:

1. Create a `music` directory in this level folder
2. Add your music file (preferably .ogg format for best pygame compatibility)
3. Name it `tower_theme.ogg` or update the level.json configuration

## Supported Audio Formats

Pygame supports various audio formats including:
- OGG Vorbis (recommended)
- MP3
- WAV
- FLAC

## Example Music Directory Structure

```
levels/1_tower/
├── music/
│   └── tower_theme.ogg
├── images/
├── maps/
└── level.json
```

The music system will gracefully handle missing files by logging an error message and continuing without music.