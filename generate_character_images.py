#!/usr/bin/env python3

import os
import json
import boto3
import base64
from PIL import Image
import io
import time

def load_level_data(levels_dir):
    """Load all level data from the levels directory"""
    levels = []

    # Check if levels directory exists
    if not os.path.exists(levels_dir):
        print(f"Levels directory not found: {levels_dir}")
        return levels

    # Iterate through each subdirectory in the levels directory
    for level_dir in os.listdir(levels_dir):
        level_path = os.path.join(levels_dir, level_dir)

        # Check if it's a directory and contains a level.json file
        if os.path.isdir(level_path):
            level_json_path = os.path.join(level_path, "level.json")

            if os.path.exists(level_json_path):
                try:
                    with open(level_json_path, 'r') as f:
                        level_data = json.load(f)

                    # Add the directory path to the level data
                    level_data['directory'] = level_path
                    levels.append(level_data)
                    print(f"Loaded level: {level_data.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"Error loading level from {level_json_path}: {e}")

    return levels

def generate_character_prompt(character_data, character_type="character", is_icon=False):
    """Generate a prompt for image generation based on character data"""
    name = character_data.get('name', 'Unknown')
    description = character_data.get('description', '')

    # Get item details if available
    items = character_data.get('items', {})
    item_details = []

    if isinstance(items, dict):
        for item_type, item in items.items():
            if isinstance(item, dict) and 'name' in item:
                item_details.append(f"{item['name']}")

    # Combine all details into a prompt
    if is_icon:
        # For map icons, create a simpler top-down view prompt
        prompt_parts = [
            f"A simple top-down pixel art icon of a {name}",
            f"Character type: {character_type}",
            "Style: pixel art, top-down view, RPG game map icon, 64x64 pixels, simple design, clear silhouette"
        ]
    else:
        # For character portraits
        prompt_parts = [
            f"A detailed fantasy RPG character portrait of a {name}",
            f"Character type: {character_type}",
        ]

        if description:
            prompt_parts.append(f"Description: {description}")

        if item_details:
            prompt_parts.append(f"Equipped with: {', '.join(item_details)}")

        # Add style guidance
        prompt_parts.append("Style: detailed digital art, fantasy RPG character portrait, 512x512 pixels, centered composition, full color, game art style")

    return ". ".join(prompt_parts)

def generate_image_with_bedrock(prompt, client):
    """Generate an image using Amazon Bedrock Stable Diffusion model"""
    try:
        print(f"Prompt: {prompt}")
        response = client.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt,
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "quality": "standard",
                    "height": 512,
                    "width": 512,
                    "seed": 42
                }
            })
        )

        response_body = json.loads(response.get('body').read())

        # Extract the base64-encoded image
        if 'images' in response_body and len(response_body['images']) > 0:
            image_b64 = response_body['images'][0]
            image_data = base64.b64decode(image_b64)
            print("Successfully generated image!")
            return Image.open(io.BytesIO(image_data))
        else:
            print(f"No image generated. Response: {response_body}")
            return None

    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def save_image(image, directory, filename):
    """Save the generated image to the specified directory"""
    # Create images directory if it doesn't exist
    images_dir = os.path.join(directory, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Save the image
    image_path = os.path.join(images_dir, filename)
    image.save(image_path)
    print(f"Saved image to {image_path}")
    return image_path

def main():
    # Initialize Bedrock client
    try:
        bedrock_client = boto3.client('bedrock-runtime')
        print("Connected to Amazon Bedrock")
    except Exception as e:
        print(f"Error connecting to Amazon Bedrock: {e}")
        return

    # Load all levels
    levels_dir = "levels"
    levels = load_level_data(levels_dir)
    print(f"Loaded {len(levels)} levels")

    # Process each level
    for level in levels:
        level_name = level.get('name', 'Unknown Level')
        level_dir = level.get('directory')
        print(f"\nProcessing level: {level_name}")

        # Generate player image
        if 'player' in level and isinstance(level['player'], dict):
            player_data = level['player']
            print(f"Generating image for player: {player_data.get('name', 'Unknown')}")

            # Generate portrait prompt
            prompt = generate_character_prompt(player_data, "player character")
            print(f"Player portrait prompt: {prompt}")

            # Generate portrait image
            player_image = generate_image_with_bedrock(prompt, bedrock_client)

            if player_image:
                # Save portrait image
                player_image_path = save_image(player_image, level_dir, "player.png")

                # Update level.json with new image path
                player_data['image'] = "images/player.png"

            # Add a delay to avoid rate limiting
            time.sleep(2)

            # Generate map icon prompt
            icon_prompt = generate_character_prompt(player_data, "player character", is_icon=True)
            print(f"Player icon prompt: {icon_prompt}")

            # Generate map icon image
            player_icon = generate_image_with_bedrock(icon_prompt, bedrock_client)

            if player_icon:
                # Save icon image
                player_icon_path = save_image(player_icon, level_dir, "player_icon.png")

                # Update level.json with new icon path
                player_data['icon'] = "images/player_icon.png"

            # Add a delay to avoid rate limiting
            time.sleep(2)

        # Generate enemy images
        if 'enemies' in level and isinstance(level['enemies'], list):
            for i, enemy_data in enumerate(level['enemies']):
                if isinstance(enemy_data, dict):
                    enemy_name = enemy_data.get('name', f"Enemy_{i}")
                    print(f"Generating image for enemy: {enemy_name}")

                    # Generate portrait prompt
                    prompt = generate_character_prompt(enemy_data, "enemy character")
                    print(f"Enemy portrait prompt: {prompt}")

                    # Generate portrait image
                    enemy_image = generate_image_with_bedrock(prompt, bedrock_client)

                    if enemy_image:
                        # Save portrait image with enemy name (sanitized for filename)
                        enemy_filename = f"enemy_{i}_{enemy_name.lower().replace(' ', '_')}.png"
                        enemy_image_path = save_image(enemy_image, level_dir, enemy_filename)

                        # Update level.json with new image path
                        enemy_data['image'] = f"images/{enemy_filename}"

                    # Add a delay to avoid rate limiting
                    time.sleep(2)

                    # Generate map icon prompt
                    icon_prompt = generate_character_prompt(enemy_data, "enemy character", is_icon=True)
                    print(f"Enemy icon prompt: {icon_prompt}")

                    # Generate map icon image
                    enemy_icon = generate_image_with_bedrock(icon_prompt, bedrock_client)

                    if enemy_icon:
                        # Save icon image
                        enemy_icon_filename = f"enemy_{i}_{enemy_name.lower().replace(' ', '_')}_icon.png"
                        enemy_icon_path = save_image(enemy_icon, level_dir, enemy_icon_filename)

                        # Update level.json with new icon path
                        enemy_data['icon'] = f"images/{enemy_icon_filename}"

                    # Add a delay to avoid rate limiting
                    time.sleep(2)

        # Save updated level.json
        try:
            level_json_path = os.path.join(level_dir, "level.json")
            with open(level_json_path, 'w') as f:
                # Remove directory key before saving
                level_copy = level.copy()
                if 'directory' in level_copy:
                    del level_copy['directory']
                json.dump(level_copy, f, indent=2)
            print(f"Updated level.json with new image paths")
        except Exception as e:
            print(f"Error updating level.json: {e}")

if __name__ == "__main__":
    main()
    print("\nImage generation complete!")
