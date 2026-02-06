"""
Multi-language script generator for ad video scenes.
Generates contextual scripts based on parameters and language.
"""

from typing import Dict


class ScriptGenerator:
    """Generates scripts for video scenes in multiple languages."""
    
    # Script templates for each scene and language
    # New structure: Scene 1 (Multi-wallpaper showcase) + Scene 2 (Play Store)
    TEMPLATES = {
        'en': {
            'scene1': "Explore divine {god_name} live wallpapers. Transform your screen with spiritual beauty. {custom_text}",
            'scene2': "Download now from Play Store and bring divine presence to your phone."
        },
        'hi': {
            'scene1': "{god_name} के दिव्य लाइव वॉलपेपर देखें। अपनी स्क्रीन को आध्यात्मिक सुंदरता से सजाएं। {custom_text}",
            'scene2': "प्ले स्टोर से अभी डाउनलोड करें और अपने फोन में दिव्यता लाएं।"
        }
    }
    
    @staticmethod
    def generate_scene1_script(god_name: str, custom_text: str, language: str) -> str:
        """
        Generate script for Scene 1 (Live Wallpaper Preview).
        
        Args:
            god_name: Name of the deity/god
            custom_text: Custom promotional text
            language: Language code ('en', 'hi', etc.)
            
        Returns:
            Formatted script text
        """
        template = ScriptGenerator.TEMPLATES.get(language, ScriptGenerator.TEMPLATES['en'])
        script = template['scene1'].format(
            god_name=god_name,
            custom_text=custom_text
        )
        return script
    
    @staticmethod
    def generate_scene2_script(language: str) -> str:
        """
        Generate script for Scene 2 (App Showcase).
        
        Args:
            language: Language code ('en', 'hi', etc.)
            
        Returns:
            Script text
        """
        template = ScriptGenerator.TEMPLATES.get(language, ScriptGenerator.TEMPLATES['en'])
        return template['scene2']
    
    @staticmethod
    def generate_scene3_script(language: str) -> str:
        """
        Generate script for Scene 3 (Play Store Install).
        
        Args:
            language: Language code ('en', 'hi', etc.)
            
        Returns:
            Script text
        """
        template = ScriptGenerator.TEMPLATES.get(language, ScriptGenerator.TEMPLATES['en'])
        return template['scene3']
    
    @staticmethod
    def generate_all_scripts(god_name: str, custom_text: str, language: str) -> Dict[str, str]:
        """
        Generate scripts for all scenes.
        
        Args:
            god_name: Name of the deity/god
            custom_text: Custom promotional text
            language: Language code
            
        Returns:
            Dictionary with keys 'scene1', 'scene2' and script values
        """
        return {
            'scene1': ScriptGenerator.generate_scene1_script(god_name, custom_text, language),
            'scene2': ScriptGenerator.generate_scene2_script(language)
        }
