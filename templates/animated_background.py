# Apply Pillow 10+ compatibility patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import moviepy_compat

"""
Animated Background Generator
Creates decorative animated backgrounds for video scenes.
"""

from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw
import numpy as np
import math


def create_rotating_mandala(duration, size=(720, 1280), rotation_speed=30):
    """
    Create a rotating mandala/Om symbol background.
    
    Args:
        duration: Duration in seconds
        size: (width, height) tuple
        rotation_speed: Degrees per second
    
    Returns:
        VideoClip with rotating mandala
    """
    width, height = size
    
    # Create mandala image
    mandala_size = min(width, height) * 2
    mandala_img = Image.new('RGBA', (mandala_size, mandala_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mandala_img)
    
    center = mandala_size // 2
    
    # Draw concentric circles with decorative patterns
    for radius in range(50, mandala_size // 2, 80):
        # Outer circle
        draw.ellipse(
            [center - radius, center - radius, center + radius, center + radius],
            outline=(255, 140, 0, 100),
            width=3
        )
        
        # Inner decorative circles
        num_circles = 12
        for i in range(num_circles):
            angle = (2 * math.pi * i) / num_circles
            x = center + int(radius * 0.8 * math.cos(angle))
            y = center + int(radius * 0.8 * math.sin(angle))
            small_r = 15
            draw.ellipse(
                [x - small_r, y - small_r, x + small_r, y + small_r],
                fill=(255, 165, 0, 80)
            )
    
    # Save mandala
    mandala_path = 'assets/temp_mandala.png'
    os.makedirs('assets', exist_ok=True)
    mandala_img.save(mandala_path)
    
    # Create rotating clip
    mandala_clip = ImageClip(mandala_path, duration=duration)
    
    # Apply rotation animation
    def rotate_frame(t):
        angle = (rotation_speed * t) % 360
        return angle
    
    mandala_clip = mandala_clip.rotate(lambda t: rotate_frame(t), expand=False)
    mandala_clip = mandala_clip.set_position('center')
    
    return mandala_clip


def create_gradient_background(duration, size=(720, 1280), colors=None):
    """
    Create an animated gradient background.
    
    Args:
        duration: Duration in seconds
        size: (width, height) tuple
        colors: List of color tuples, default is orange/red theme
    
    Returns:
        VideoClip with gradient background
    """
    if colors is None:
        colors = [
            (220, 20, 60),    # Crimson
            (255, 69, 0),     # Orange Red
            (255, 140, 0),    # Dark Orange
        ]
    
    width, height = size
    
    # Create gradient image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Vertical gradient
    for y in range(height):
        # Interpolate between colors
        ratio = y / height
        if ratio < 0.5:
            # First half: color[0] to color[1]
            t = ratio * 2
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * t)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * t)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * t)
        else:
            # Second half: color[1] to color[2]
            t = (ratio - 0.5) * 2
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * t)
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * t)
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * t)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Save gradient
    gradient_path = 'assets/temp_gradient.png'
    os.makedirs('assets', exist_ok=True)
    img.save(gradient_path)
    
    # Create clip
    gradient_clip = ImageClip(gradient_path, duration=duration)
    
    return gradient_clip


def create_animated_background(duration, size=(720, 1280), style='mandala'):
    """
    Create an animated decorative background.
    
    Args:
        duration: Duration in seconds
        size: (width, height) tuple
        style: 'mandala' or 'gradient'
    
    Returns:
        CompositeVideoClip with animated background
    """
    width, height = size
    
    # Base gradient
    gradient = create_gradient_background(duration, size)
    
    if style == 'mandala':
        # Add rotating mandala overlay
        mandala = create_rotating_mandala(duration, size, rotation_speed=20)
        mandala = mandala.set_opacity(0.3)  # Semi-transparent
        
        # Composite
        background = CompositeVideoClip(
            [gradient, mandala],
            size=size
        )
    else:
        background = gradient
    
    return background


if __name__ == '__main__':
    # Test the animated background
    print("Creating test animated background...")
    bg = create_animated_background(5, style='mandala')
    bg.write_videofile('output/test_background.mp4', fps=30)
    print("[OK] Test background created: output/test_background.mp4")
