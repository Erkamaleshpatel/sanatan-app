# Apply Pillow 10+ compatibility patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import moviepy_compat

"""
Scene 3: Play Store Install
Shows Play Store listing with install animation.
"""

from moviepy.editor import (
    ImageClip, CompositeVideoClip, AudioFileClip,
    VideoFileClip
)
from PIL import Image, ImageDraw, ImageFont
import os


class Scene3PlayStoreInstall:
    """Creates the Play Store install scene."""
    
    def __init__(self, phone_mockup_path: str, playstore_mockup_path: str = None):
        """
        Initialize Scene 3.
        
        Args:
            phone_mockup_path: Path to phone frame PNG
            playstore_mockup_path: Path to Play Store screenshot
        """
        self.phone_mockup_path = phone_mockup_path
        self.playstore_mockup_path = playstore_mockup_path
    
    def create(
        self,
        voiceover_path: str,
        duration: float = None
    ) -> VideoFileClip:
        """
        Create Scene 3 video clip.
        
        Args:
            voiceover_path: Path to voiceover audio file
            duration: Scene duration (if None, uses voiceover duration)
            
        Returns:
            VideoFileClip for Scene 3
        """
        # Load voiceover to get duration
        voiceover = AudioFileClip(voiceover_path)
        scene_duration = duration or voiceover.duration
        
        # If no Play Store mockup provided, create placeholder
        if not self.playstore_mockup_path or not os.path.exists(self.playstore_mockup_path):
            playstore_image = self._create_placeholder_playstore()
            self.playstore_mockup_path = 'assets/generated_playstore.png'
            playstore_image.save(self.playstore_mockup_path)
        
        # Load Play Store screenshot
        playstore_clip = ImageClip(self.playstore_mockup_path, duration=scene_duration)
        
        # Phone screen dimensions
        screen_width = 720
        screen_height = 1280
        
        # Resize to fit phone screen using tuple parameter (MoviePy 1.0.3 + Pillow 11+ compatible)
        playstore_clip = playstore_clip.resize((screen_width, screen_height))
        
        # Load phone mockup
        phone_mockup = ImageClip(self.phone_mockup_path, duration=scene_duration)
        
        # Position elements
        video_width = 1080
        video_height = 1920
        
        playstore_clip = playstore_clip.set_position(('center', 'center'))
        phone_mockup = phone_mockup.set_position(('center', 'center'))
        
        # Composite: Play Store screen behind phone frame
        composite = CompositeVideoClip(
            [playstore_clip, phone_mockup],
            size=(video_width, video_height)
        ).set_duration(scene_duration)
        
        # Add voiceover
        composite = composite.set_audio(voiceover)
        
        return composite
    
    def _create_placeholder_playstore(self) -> Image.Image:
        """Create a placeholder Play Store listing image."""
        width, height = 720, 1280
        img = Image.new('RGB', (width, height), color='#ffffff')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_subtitle = ImageFont.truetype("arial.ttf", 40)
            font_button = ImageFont.truetype("arial.ttf", 50)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_button = ImageFont.load_default()
        
        # App icon placeholder
        icon_size = 200
        icon_x = 50
        icon_y = 100
        draw.rectangle(
            [icon_x, icon_y, icon_x + icon_size, icon_y + icon_size],
            fill='#4285f4'
        )
        
        # App name
        app_name = "Divine Wallpapers"
        draw.text((icon_x + icon_size + 30, icon_y + 30), app_name, fill='#000000', font=font_title)
        
        # Developer name
        dev_name = "Spiritual Apps"
        draw.text((icon_x + icon_size + 30, icon_y + 100), dev_name, fill='#666666', font=font_subtitle)
        
        # Rating
        rating = "★★★★★ 4.8"
        draw.text((icon_x + icon_size + 30, icon_y + 150), rating, fill='#01875f', font=font_subtitle)
        
        # Install button
        button_y = icon_y + icon_size + 100
        button_width = 620
        button_height = 120
        button_x = (width - button_width) // 2
        
        # Green install button
        draw.rectangle(
            [button_x, button_y, button_x + button_width, button_y + button_height],
            fill='#01875f'
        )
        
        # Install text
        install_text = "Install"
        bbox = draw.textbbox((0, 0), install_text, font=font_button)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (button_x + (button_width - text_width) // 2, button_y + (button_height - text_height) // 2),
            install_text,
            fill='#ffffff',
            font=font_button
        )
        
        # Screenshots section
        screenshot_y = button_y + button_height + 80
        draw.text((50, screenshot_y), "Screenshots", fill='#000000', font=font_title)
        
        # Screenshot placeholders
        screenshot_width = 200
        screenshot_height = 350
        screenshot_margin = 20
        screenshot_start_y = screenshot_y + 80
        
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
        for i, color in enumerate(colors):
            x = 50 + i * (screenshot_width + screenshot_margin)
            draw.rectangle(
                [x, screenshot_start_y, x + screenshot_width, screenshot_start_y + screenshot_height],
                fill=color
            )
        
        return img
