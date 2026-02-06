# Apply Pillow 10+ compatibility patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import moviepy_compat

"""
Scene 2: App Showcase
Displays the app interface with multiple wallpaper options.
"""

from moviepy.editor import (
    ImageClip, CompositeVideoClip, AudioFileClip,
    VideoFileClip
)
from PIL import Image, ImageDraw, ImageFont
import os


class Scene2AppShowcase:
    """Creates the app showcase scene."""
    
    def __init__(self, app_showcase_path: str = None):
        """
        Initialize Scene 2.
        
        Args:
            app_showcase_path: Path to app interface mockup image
        """
        self.app_showcase_path = app_showcase_path
    
    def create(
        self,
        voiceover_path: str,
        duration: float = None
    ) -> VideoFileClip:
        """
        Create Scene 2 video clip.
        
        Args:
            voiceover_path: Path to voiceover audio file
            duration: Scene duration (if None, uses voiceover duration)
            
        Returns:
            VideoFileClip for Scene 2
        """
        # Load voiceover to get duration
        voiceover = AudioFileClip(voiceover_path)
        scene_duration = duration or voiceover.duration
        
        # If no showcase image provided, create a simple placeholder
        if not self.app_showcase_path or not os.path.exists(self.app_showcase_path):
            showcase_image = self._create_placeholder_showcase()
            self.app_showcase_path = 'assets/generated_showcase.png'
            showcase_image.save(self.app_showcase_path)
        
        # Load showcase image
        showcase_clip = ImageClip(self.app_showcase_path, duration=scene_duration)
        
        # Apply fade in/out transitions
        showcase_clip = showcase_clip.fadein(0.5).fadeout(0.5)
        
        # Create composite
        video_width = 1080
        video_height = 1920
        
        # Resize to fit using tuple parameter (MoviePy 1.0.3 + Pillow 11+ compatible)
        showcase_clip = showcase_clip.resize((video_width, video_height))
        showcase_clip = showcase_clip.set_position('center')
        
        composite = CompositeVideoClip(
            [showcase_clip],
            size=(video_width, video_height)
        ).set_duration(scene_duration)
        
        # Add voiceover
        composite = composite.set_audio(voiceover)
        
        return composite
    
    def _create_placeholder_showcase(self) -> Image.Image:
        """Create a placeholder app showcase image."""
        width, height = 1080, 1920
        img = Image.new('RGB', (width, height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Add title
        try:
            font_large = ImageFont.truetype("arial.ttf", 80)
            font_small = ImageFont.truetype("arial.ttf", 50)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "Divine Wallpapers"
        bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = bbox[2] - bbox[0]
        draw.text(
            ((width - title_width) // 2, 200),
            title,
            fill='#ffffff',
            font=font_large
        )
        
        # Subtitle
        subtitle = "Hundreds of Live Wallpapers"
        bbox = draw.textbbox((0, 0), subtitle, font=font_small)
        subtitle_width = bbox[2] - bbox[0]
        draw.text(
            ((width - subtitle_width) // 2, 320),
            subtitle,
            fill='#aaaaaa',
            font=font_small
        )
        
        # Draw placeholder grid for wallpapers
        grid_cols = 3
        grid_rows = 4
        cell_width = 300
        cell_height = 400
        margin = 40
        
        start_x = (width - (grid_cols * cell_width + (grid_cols - 1) * margin)) // 2
        start_y = 500
        
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7', '#a29bfe',
                  '#fd79a8', '#fdcb6e', '#e17055', '#74b9ff', '#a29bfe', '#dfe6e9']
        
        for row in range(grid_rows):
            for col in range(grid_cols):
                x = start_x + col * (cell_width + margin)
                y = start_y + row * (cell_height + margin)
                color = colors[(row * grid_cols + col) % len(colors)]
                draw.rectangle([x, y, x + cell_width, y + cell_height], fill=color)
        
        return img
