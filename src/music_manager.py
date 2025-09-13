"""
Music Manager Module for Q-Quest Game

This module handles all music-related operations including:
- Pygame mixer initialization
- Loading and playing background music
- Volume control and fade effects
- Music transitions between levels
"""

import pygame
import os
import sys


class MusicManager:
    """Centralized music management system for the game"""
    
    def __init__(self):
        self.initialized = False
        self.current_music = None
        self.volume = 0.7  # Default volume (70%)
        self.fade_duration = 1000  # Fade duration in milliseconds
        
    def initialize(self):
        """Initialize pygame mixer for music playback"""
        try:
            # Initialize mixer with appropriate settings
            # 44100 Hz, 16-bit, stereo, 1024 byte buffer
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self.initialized = True
            print("Music system initialized successfully")
            return True
        except pygame.error as e:
            print(f"Failed to initialize music system: {e}")
            self.initialized = False
            return False
    
    def load_music(self, music_path):
        """
        Load a music file for playback
        
        Args:
            music_path (str): Path to the music file
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not self.initialized:
            print("Music system not initialized")
            return False
            
        if not os.path.exists(music_path):
            print(f"Music file not found: {music_path}")
            return False
            
        try:
            pygame.mixer.music.load(music_path)
            self.current_music = music_path
            print(f"Loaded music: {os.path.basename(music_path)}")
            return True
        except pygame.error as e:
            print(f"Failed to load music file {music_path}: {e}")
            return False
    
    def play_music(self, loops=-1, fade_in=True):
        """
        Play the currently loaded music
        
        Args:
            loops (int): Number of times to loop (-1 for infinite)
            fade_in (bool): Whether to fade in the music
        """
        if not self.initialized:
            return
            
        try:
            if fade_in:
                pygame.mixer.music.play(loops, fade_ms=self.fade_duration)
            else:
                pygame.mixer.music.play(loops)
            
            pygame.mixer.music.set_volume(self.volume)
            print(f"Playing music: {os.path.basename(self.current_music) if self.current_music else 'Unknown'}")
        except pygame.error as e:
            print(f"Failed to play music: {e}")
    
    def stop_music(self, fade_out=True):
        """
        Stop the currently playing music
        
        Args:
            fade_out (bool): Whether to fade out the music
        """
        if not self.initialized:
            return
            
        try:
            if fade_out and pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(self.fade_duration)
            else:
                pygame.mixer.music.stop()
            print("Music stopped")
        except pygame.error as e:
            print(f"Failed to stop music: {e}")
    
    def pause_music(self):
        """Pause the currently playing music"""
        if not self.initialized:
            return
            
        try:
            pygame.mixer.music.pause()
            print("Music paused")
        except pygame.error as e:
            print(f"Failed to pause music: {e}")
    
    def unpause_music(self):
        """Unpause the currently paused music"""
        if not self.initialized:
            return
            
        try:
            pygame.mixer.music.unpause()
            print("Music unpaused")
        except pygame.error as e:
            print(f"Failed to unpause music: {e}")
    
    def set_volume(self, volume):
        """
        Set the music volume
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        if not self.initialized:
            return
            
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        try:
            pygame.mixer.music.set_volume(self.volume)
            print(f"Music volume set to: {self.volume:.1%}")
        except pygame.error as e:
            print(f"Failed to set volume: {e}")
    
    def is_playing(self):
        """
        Check if music is currently playing
        
        Returns:
            bool: True if music is playing, False otherwise
        """
        if not self.initialized:
            return False
            
        try:
            return pygame.mixer.music.get_busy()
        except pygame.error:
            return False
    
    def load_and_play_level_music(self, level_data):
        """
        Load and play music for a specific level
        
        Args:
            level_data (dict): Level configuration data
            
        Returns:
            bool: True if music was loaded and started, False otherwise
        """
        if not self.initialized:
            return False
            
        # Check if level has music configuration
        music_config = level_data.get('music')
        if not music_config:
            print("No music configuration found for level")
            return False
            
        # Get music file path
        music_file = music_config.get('file')
        if not music_file:
            print("No music file specified in level configuration")
            return False
            
        # Construct full path to music file
        level_directory = level_data.get('directory')
        if level_directory:
            music_path = os.path.join(level_directory, music_file)
        else:
            music_path = music_file
            
        # Stop current music if playing
        if self.is_playing():
            self.stop_music(fade_out=True)
            # Wait a bit for fade out to complete
            pygame.time.wait(self.fade_duration)
        
        # Load and play new music
        if self.load_music(music_path):
            # Get music settings from configuration
            volume = music_config.get('volume', self.volume)
            loops = music_config.get('loops', -1)  # Default to infinite loop
            fade_in = music_config.get('fade_in', True)
            
            # Set volume if specified
            if volume != self.volume:
                self.set_volume(volume)
            
            # Play the music
            self.play_music(loops=loops, fade_in=fade_in)
            return True
        
        return False


# Global music manager instance
music_manager = MusicManager()


def initialize_music_system():
    """Initialize the global music system"""
    return music_manager.initialize()


def get_music_manager():
    """Get the global music manager instance"""
    return music_manager