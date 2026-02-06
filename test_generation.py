"""
Test script to generate a sample video.
This demonstrates the programmatic usage of the video generation system.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templates.base_template import generate_video
from PIL import Image, ImageDraw, ImageFont

def create_sample_wallpapers(count=3):
    """Create multiple sample wallpapers for testing."""
    wallpaper_paths = []
    
    for i in range(count):
        width, height = 1080, 1920
        img = Image.new('RGB', (width, height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect with different colors for each
        colors = [
            ('#1a1a2e', '#8a2be2'),  # Purple
            ('#0f2027', '#2c5364'),  # Blue
            ('#360033', '#0b8793'),  # Teal
        ]
        start_color, end_color = colors[i % len(colors)]
        
        for y in range(height):
            r1, g1, b1 = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
            r2, g2, b2 = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)
            
            r = int(r1 + (r2 - r1) * y / height)
            g = int(g1 + (g2 - g1) * y / height)
            b = int(b1 + (b2 - b1) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except:
            font = ImageFont.load_default()
        
        texts = ["ॐ", "🕉️", "☸️"]
        text = texts[i % len(texts)]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (width - text_width) // 2
        y_pos = (height - text_height) // 2
        
        # Draw with glow effect
        for offset in range(10, 0, -1):
            alpha = int(255 * (1 - offset / 10))
            draw.text((x, y_pos), text, fill=(255, 215, 0, alpha), font=font)
        
        draw.text((x, y_pos), text, fill='#FFD700', font=font)
        
        # Save
        output_path = f'assets/sample_wallpaper_{i+1}.jpg'
        os.makedirs('assets', exist_ok=True)
        img.save(output_path)
        print(f"[OK] Created sample wallpaper {i+1}: {output_path}")
        wallpaper_paths.append(output_path)
    
    return wallpaper_paths


def test_video_generation():
    """Test the video generation system."""
    print("=" * 60)
    print("Live Wallpaper Ad Generator - Test Script")
    print("=" * 60)
    
    # Create sample wallpapers
    print("\n1. Creating sample wallpapers...")
    wallpapers = create_sample_wallpapers(count=3)
    
    # Test parameters
    test_cases = [
        {
            'name': 'Single Wallpaper - English',
            'params': {
                'wallpaper': wallpapers[0],  # Single wallpaper (backward compatible)
                'god_name': 'Lord Shiva',
                'custom_text': 'Feel the divine presence',
                'language_code': 'en'
            }
        },
        {
            'name': 'Multi-Wallpaper - English (3 wallpapers)',
            'params': {
                'wallpapers': wallpapers,  # Multiple wallpapers (new feature)
                'god_name': 'Lord Krishna',
                'custom_text': 'Experience divine beauty',
                'language_code': 'en'
            }
        },
        {
            'name': 'Multi-Wallpaper - Hindi (3 wallpapers)',
            'params': {
                'wallpapers': wallpapers,
                'god_name': 'भगवान कृष्ण',
                'custom_text': 'दिव्य सुंदरता का अनुभव करें',
                'language_code': 'hi'
            }
        }
    ]
    
    # Generate videos
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i + 1}. Generating video: {test_case['name']}")
        print("-" * 60)
        
        try:
            output_path = generate_video(test_case['params'])
            print(f"\n[OK] SUCCESS: {test_case['name']}")
            print(f"  Output: {output_path}")
        except Exception as e:
            print(f"\n✗ FAILED: {test_case['name']}")
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == '__main__':
    test_video_generation()
