# Apply Pillow 10+ compatibility patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import moviepy_compat

"""
Scene 1: Live Wallpaper Preview
Displays a phone mockup with the wallpaper inserted inside the screen.
"""

from moviepy.editor import (
    VideoFileClip, ImageClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)
from PIL import Image
import os


class Scene1WallpaperPreview:
    """Creates the live wallpaper preview scene."""
    
    def __init__(self, phone_mockup_path: str):
        """
        Initialize Scene 1.
        
        Args:
            phone_mockup_path: Path to phone frame PNG with transparent center
        """
        self.phone_mockup_path = phone_mockup_path
    
    def create(
        self,
        wallpaper_path: str,
        voiceover_path: str,
        duration: float = None
    ) -> VideoFileClip:
        """
        Create Scene 1 video clip.
        
        Args:
            wallpaper_path: Path to wallpaper image or video
            voiceover_path: Path to voiceover audio file
            duration: Scene duration (if None, uses voiceover duration)
            
        Returns:
            VideoFileClip for Scene 1
        """
        # Load voiceover to get duration
        voiceover = AudioFileClip(voiceover_path)
        scene_duration = duration or voiceover.duration
        
        # Determine if wallpaper is image or video
        is_video = wallpaper_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
        
        if is_video:
            wallpaper_clip = VideoFileClip(wallpaper_path)
            # Loop if needed
            if wallpaper_clip.duration < scene_duration:
                wallpaper_clip = wallpaper_clip.loop(duration=scene_duration)
            else:
                wallpaper_clip = wallpaper_clip.subclip(0, scene_duration)
        else:
            wallpaper_clip = ImageClip(wallpaper_path, duration=scene_duration)
        
        # Phone screen dimensions (adjust based on your mockup)
        # These are relative positions - adjust for your specific phone mockup
        screen_width = 720
        screen_height = 1280
        
        # Resize wallpaper to fit phone screen using tuple parameter
        # This works with MoviePy 1.0.3 and Pillow 11+
        wallpaper_clip = wallpaper_clip.resize((screen_width, screen_height))
        
        # Load phone mockup
        phone_mockup = ImageClip(self.phone_mockup_path, duration=scene_duration)
        
        # Position wallpaper in center (behind phone frame)
        video_width = 1080
        video_height = 1920
        
        wallpaper_clip = wallpaper_clip.set_position(('center', 'center'))
        phone_mockup = phone_mockup.set_position(('center', 'center'))
        
        # Composite: wallpaper behind phone frame
        composite = CompositeVideoClip(
            [wallpaper_clip, phone_mockup],
            size=(video_width, video_height)
        ).set_duration(scene_duration)
        
        # Add voiceover
        composite = composite.set_audio(voiceover)
        
        return composite
