# Apply Pillow 10+ compatibility patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import moviepy_compat

"""
Multi-Wallpaper Showcase Scene
Displays multiple wallpapers in sequence with smooth transitions.
Similar to reference video style.
"""

from moviepy.editor import (VideoFileClip, ImageClip, CompositeVideoClip, 
                            concatenate_videoclips, AudioFileClip, ColorClip)
from PIL import Image, ImageDraw
import os
from templates.animated_background import create_animated_background


class MultiWallpaperScene:
    """Scene that showcases multiple wallpapers in sequence."""
    
    def __init__(self, phone_mockup_path=None):
        """
        Initialize the multi-wallpaper scene.
        
        Args:
            phone_mockup_path: Path to phone mockup PNG (optional)
        """
        self.phone_mockup_path = phone_mockup_path or self._generate_phone_mockup()
    
    def _generate_phone_mockup(self):
        """Generate a simple phone mockup if none provided."""
        width, height = 800, 1600
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Phone outline
        border_radius = 60
        border_width = 15
        
        # Outer border (phone body)
        draw.rounded_rectangle(
            [0, 0, width, height],
            radius=border_radius,
            fill=(30, 30, 30, 255),
            outline=(200, 200, 200, 255),
            width=border_width
        )
        
        # Screen area (transparent center)
        screen_margin = 40
        draw.rounded_rectangle(
            [screen_margin, screen_margin, 
             width - screen_margin, height - screen_margin],
            radius=border_radius - 20,
            fill=(0, 0, 0, 0)
        )
        
        # Save mockup
        mockup_path = 'assets/phone_mockup_multi.png'
        os.makedirs('assets', exist_ok=True)
        img.save(mockup_path)
        
        return mockup_path
    
    def create(self, wallpapers, voiceover_path, duration_per_wallpaper=4):
        """
        Create the multi-wallpaper showcase scene.
        
        Args:
            wallpapers: List of wallpaper file paths (images or videos)
            voiceover_path: Path to voiceover audio file
            duration_per_wallpaper: Seconds to show each wallpaper
        
        Returns:
            VideoClip of the complete scene
        """
        if not wallpapers or len(wallpapers) == 0:
            raise ValueError("At least one wallpaper is required")
        
        # Get voiceover duration
        voiceover = AudioFileClip(voiceover_path)
        voiceover_duration = voiceover.duration
        
        # Calculate scene duration
        total_wallpaper_time = len(wallpapers) * duration_per_wallpaper
        scene_duration = max(voiceover_duration, total_wallpaper_time)
        
        # Adjust duration per wallpaper if needed
        if total_wallpaper_time < voiceover_duration:
            duration_per_wallpaper = voiceover_duration / len(wallpapers)
        
        print(f"  Creating Multi-Wallpaper Scene...")
        print(f"  - {len(wallpapers)} wallpapers")
        print(f"  - {duration_per_wallpaper:.1f}s per wallpaper")
        print(f"  - Total duration: {scene_duration:.1f}s")
        
        # Video dimensions
        video_width = 1080
        video_height = 1920
        
        # Phone screen dimensions (inside mockup)
        screen_width = 720
        screen_height = 1280
        
        # Create animated background
        background = create_animated_background(
            duration=scene_duration,
            size=(video_width, video_height),
            style='mandala'
        )
        
        # Load phone mockup
        phone_mockup = ImageClip(self.phone_mockup_path, duration=scene_duration)
        phone_mockup = phone_mockup.resize((screen_width, screen_height))
        phone_mockup = phone_mockup.set_position('center')
        
        # Create wallpaper clips with transitions
        wallpaper_clips = []
        transition_duration = 0.5  # Crossfade duration
        
        for i, wallpaper_path in enumerate(wallpapers):
            # Load wallpaper (image or video)
            if wallpaper_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                wallpaper_clip = VideoFileClip(wallpaper_path)
                # Loop if too short
                if wallpaper_clip.duration < duration_per_wallpaper:
                    wallpaper_clip = wallpaper_clip.loop(duration=duration_per_wallpaper)
                else:
                    wallpaper_clip = wallpaper_clip.subclip(0, duration_per_wallpaper)
            else:
                wallpaper_clip = ImageClip(wallpaper_path, duration=duration_per_wallpaper)
            
            # Resize wallpaper to fit phone screen using tuple parameter
            # This works with MoviePy 1.0.3 and Pillow 10+
            wallpaper_clip = wallpaper_clip.resize((screen_width, screen_height))
            
            # Add fade in/out for smooth transitions
            if i == 0:
                # First wallpaper: fade in only
                wallpaper_clip = wallpaper_clip.fadein(transition_duration)
            elif i == len(wallpapers) - 1:
                # Last wallpaper: fade out only
                wallpaper_clip = wallpaper_clip.fadeout(transition_duration)
            else:
                # Middle wallpapers: fade in and out
                wallpaper_clip = wallpaper_clip.fadein(transition_duration)
                wallpaper_clip = wallpaper_clip.fadeout(transition_duration)
            
            wallpaper_clips.append(wallpaper_clip)
        
        # Concatenate wallpapers with crossfade
        if len(wallpaper_clips) == 1:
            wallpapers_sequence = wallpaper_clips[0]
        else:
            # Use crossfadein for smooth transitions
            for i in range(1, len(wallpaper_clips)):
                wallpaper_clips[i] = wallpaper_clips[i].crossfadein(transition_duration)
            
            wallpapers_sequence = concatenate_videoclips(
                wallpaper_clips,
                method="compose",
                padding=-transition_duration  # Overlap for crossfade
            )
        
        # Position wallpapers in center
        wallpapers_sequence = wallpapers_sequence.set_position('center')
        
        # Composite: background + wallpapers + phone mockup
        composite = CompositeVideoClip(
            [background, wallpapers_sequence, phone_mockup],
            size=(video_width, video_height)
        )
        
        # Set duration and add voiceover
        composite = composite.set_duration(scene_duration)
        composite = composite.set_audio(voiceover)
        
        return composite


if __name__ == '__main__':
    # Test the scene
    print("Testing multi-wallpaper scene...")
    scene = MultiWallpaperScene()
    
    # Create test wallpapers
    test_wallpapers = ['assets/sample_wallpaper.jpg'] * 3
    
    # Note: This is just a structure test, actual voiceover needed for full test
    print("(✓) Multi-wallpaper scene module created successfully")
