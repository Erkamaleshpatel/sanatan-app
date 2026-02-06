"""
Base template orchestrator for ad video generation.
Coordinates all scenes, voiceovers, and final composition.
"""

from moviepy.editor import (
    concatenate_videoclips, AudioFileClip,
    CompositeVideoClip, VideoFileClip
)
import os
from typing import Dict, List, Union
from scripts.script_generator import ScriptGenerator
from audio.voice_generator import VoiceGenerator
from templates.scene_multi_wallpapers import MultiWallpaperScene
from templates.scene3_install import Scene3PlayStoreInstall


class VideoTemplate:
    """Main video template orchestrator."""
    
    def __init__(self, assets_dir: str = 'assets', output_dir: str = 'output'):
        """
        Initialize video template.
        
        Args:
            assets_dir: Directory containing asset files
            output_dir: Directory for output videos
        """
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.voice_generator = VoiceGenerator()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'temp_audio'), exist_ok=True)
    
    def generate_video(self, params: Dict) -> str:
        """
        Generate complete ad video from parameters.
        
        Args:
            params: Dictionary containing:
                - wallpaper: Path to single wallpaper (backward compatible)
                  OR
                - wallpapers: List of wallpaper paths (new multi-image feature)
                - god_name: Name of deity
                - custom_text: Custom promotional text
                - language_code: Language code (en, hi, etc.)
                
        Returns:
            Path to generated video file
        """
        # Support both single wallpaper and multiple wallpapers
        if 'wallpapers' in params:
            wallpapers = params['wallpapers']
            if not isinstance(wallpapers, list):
                wallpapers = [wallpapers]
        elif 'wallpaper' in params:
            wallpapers = [params['wallpaper']]
        else:
            raise ValueError("Either 'wallpaper' or 'wallpapers' must be provided")
        
        god_name = params['god_name']
        custom_text = params.get('custom_text', '')
        language = params['language_code']
        
        try:
            print(f"Generating video for {god_name} in language: {language}")
        except UnicodeEncodeError:
            print(f"Generating video in language: {language}")
        print(f"Using {len(wallpapers)} wallpaper(s)")
        
        # Step 1: Generate scripts for all scenes
        print("Step 1: Generating scripts...")
        scripts = ScriptGenerator.generate_all_scripts(god_name, custom_text, language)
        try:
            print(f"  Scene 1: {scripts['scene1']}")
            print(f"  Scene 2: {scripts['scene2']}")
        except UnicodeEncodeError:
            print("  Scene 1: [Script generated]")
            print("  Scene 2: [Script generated]")
        
        # Step 2: Generate voiceovers
        print("\nStep 2: Generating voiceovers...")
        voiceover_paths = {}
        voiceover_durations = {}
        
        for scene_name, script_text in scripts.items():
            audio_path = os.path.join(self.output_dir, 'temp_audio', f'{scene_name}_vo.mp3')
            path, duration = self.voice_generator.generate_voiceover(
                script_text, language, audio_path
            )
            voiceover_paths[scene_name] = path
            voiceover_durations[scene_name] = duration
            print(f"  {scene_name}: {duration:.2f}s")
        
        # Step 3: Create scenes
        print("\nStep 3: Creating scenes...")
        
        # Asset paths
        phone_mockup = os.path.join(self.assets_dir, 'phone_mockup.png')
        playstore_mockup = os.path.join(self.assets_dir, 'playstore.png')
        
        # Create phone mockup if it doesn't exist
        if not os.path.exists(phone_mockup):
            print("  Creating phone mockup...")
            self._create_phone_mockup(phone_mockup)
        
        # Scene 1: Multi-Wallpaper Showcase
        print(f"  Creating Scene 1: Multi-Wallpaper Showcase ({len(wallpapers)} wallpapers)...")
        scene1 = MultiWallpaperScene(phone_mockup)
        scene1_clip = scene1.create(
            wallpapers=wallpapers,
            voiceover_path=voiceover_paths['scene1'],
            duration_per_wallpaper=4  # 4 seconds per wallpaper
        )
        
        # Scene 2: Play Store Install
        print("  Creating Scene 2: Play Store Install...")
        scene2 = Scene3PlayStoreInstall(phone_mockup, playstore_mockup)
        scene2_clip = scene2.create(
            voiceover_paths['scene2'],
            voiceover_durations['scene2']
        )
        
        # Step 4: Concatenate scenes
        print("\nStep 4: Concatenating scenes...")
        final_video = concatenate_videoclips([scene1_clip, scene2_clip])
        
        # Step 5: Add background music (optional)
        background_music_path = os.path.join(self.assets_dir, 'background_music.mp3')
        if os.path.exists(background_music_path):
            print("Step 5: Adding background music...")
            bg_music = AudioFileClip(background_music_path)
            
            # Loop background music to match video duration
            if bg_music.duration < final_video.duration:
                num_loops = int(final_video.duration / bg_music.duration) + 1
                bg_music = concatenate_videoclips([bg_music] * num_loops)
            
            bg_music = bg_music.subclip(0, final_video.duration)
            
            # Lower volume of background music
            bg_music = bg_music.volumex(0.2)
            
            # Mix with existing audio
            from moviepy.audio.AudioClip import CompositeAudioClip
            final_audio = CompositeAudioClip([final_video.audio, bg_music])
            final_video = final_video.set_audio(final_audio)
        
        # Step 6: Render final video
        print("\nStep 6: Rendering final video...")
        output_filename = f"{god_name.replace(' ', '_')}_{language}_ad.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=os.path.join(self.output_dir, 'temp_audio', 'temp-audio.m4a'),
            remove_temp=True
        )
        
        # Cleanup
        scene1_clip.close()
        scene2_clip.close()
        final_video.close()
        
        try:
            print(f"\nVideo generated successfully: {output_path}")
        except UnicodeEncodeError:
            print("\nVideo generated successfully!")
        return output_path
    
    def _create_phone_mockup(self, output_path: str):
        """Create a simple phone mockup frame."""
        from PIL import Image, ImageDraw
        
        # Create phone frame
        width, height = 1080, 1920
        img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Phone dimensions
        phone_width = 800
        phone_height = 1600
        phone_x = (width - phone_width) // 2
        phone_y = (height - phone_height) // 2
        
        # Draw phone outline (thick border)
        border_width = 20
        draw.rectangle(
            [phone_x - border_width, phone_y - border_width,
             phone_x + phone_width + border_width, phone_y + phone_height + border_width],
            fill='#2c3e50'
        )
        
        # Draw screen area (transparent center)
        draw.rectangle(
            [phone_x, phone_y, phone_x + phone_width, phone_y + phone_height],
            fill=(0, 0, 0, 0)
        )
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)


def generate_video(params: Dict) -> str:
    """
    Convenience function to generate video.
    
    Args:
        params: Video parameters
        
    Returns:
        Path to generated video
    """
    template = VideoTemplate()
    return template.generate_video(params)
