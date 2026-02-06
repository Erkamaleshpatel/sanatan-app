"""
Voice generation abstraction layer.
Provides a clean interface for TTS providers that can be easily swapped.
"""

from abc import ABC, abstractmethod
from gtts import gTTS
import os
from typing import Tuple


class VoiceProvider(ABC):
    """Abstract base class for voice generation providers."""
    
    @abstractmethod
    def generate(self, text: str, language: str, output_path: str) -> Tuple[str, float]:
        """
        Generate voice audio from text.
        
        Args:
            text: The text to convert to speech
            language: Language code (e.g., 'en', 'hi')
            output_path: Path where audio file should be saved
            
        Returns:
            Tuple of (audio_file_path, duration_in_seconds)
        """
        pass


class GTTSProvider(VoiceProvider):
    """Google Text-to-Speech provider implementation."""
    
    def __init__(self, slow=False):
        """
        Initialize GTTS provider.
        
        Args:
            slow: If True, uses slower speech rate
        """
        self.slow = slow
    
    def generate(self, text: str, language: str, output_path: str) -> Tuple[str, float]:
        """Generate voice using Google TTS."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=self.slow)
        tts.save(output_path)
        
        # Get duration using moviepy
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(output_path)
        duration = audio.duration
        audio.close()
        
        return output_path, duration


class VoiceGenerator:
    """Main voice generator class that uses a provider."""
    
    def __init__(self, provider: VoiceProvider = None):
        """
        Initialize voice generator.
        
        Args:
            provider: Voice provider to use. Defaults to GTTSProvider.
        """
        self.provider = provider or GTTSProvider()
    
    def generate_voiceover(self, text: str, language: str, output_path: str) -> Tuple[str, float]:
        """
        Generate voiceover audio.
        
        Args:
            text: Script text to convert to speech
            language: Language code
            output_path: Where to save the audio file
            
        Returns:
            Tuple of (audio_file_path, duration_in_seconds)
        """
        return self.provider.generate(text, language, output_path)


# Example usage for future providers:
# class ElevenLabsProvider(VoiceProvider):
#     def __init__(self, api_key: str, voice_id: str):
#         self.api_key = api_key
#         self.voice_id = voice_id
#     
#     def generate(self, text: str, language: str, output_path: str) -> Tuple[str, float]:
#         # Implementation for ElevenLabs API
#         pass
