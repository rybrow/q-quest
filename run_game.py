#!/usr/bin/env python3

import os
import sys
import pygame
import traceback
import argparse
from src.main import main

def parse_arguments():
    parser = argparse.ArgumentParser(description='Q-Quest! - A Turn Based RPG')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()

try:
    args = parse_arguments()
    main(debug_mode=args.debug)
except Exception as e:
    print(f"Error running game: {e}")
    print(traceback.format_exc())
    pygame.quit()
    sys.exit(1)
