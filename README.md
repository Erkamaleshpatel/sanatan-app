# Live Wallpaper Ad Video Generator

An automated, parameterized ad video generation system for Live Wallpaper mobile applications. Built with Python and MoviePy, this system creates professional promotional videos with voiceovers in multiple languages.

## 🎯 Features

- **3-Scene Template Architecture**: Modular design with independent scene components
- **Multi-language Support**: English and Hindi voiceovers with easy extensibility
- **Voice Abstraction Layer**: Clean interface for swapping TTS providers
- **Dynamic Timing**: Scene duration auto-adjusts to voiceover length
- **Web Interface**: Simple Flask-based upload form
- **Parameterized Generation**: Fully driven by input parameters

## 📁 Project Structure

```
sanatan-app/
├── templates/
│   ├── base_template.py      # Main video orchestrator
│   ├── scene1_wallpaper.py   # Live wallpaper preview scene
│   ├── scene2_showcase.py    # App showcase scene
│   └── scene3_install.py     # Play Store install scene
├── audio/
│   └── voice_generator.py    # Voice abstraction layer
├── scripts/
│   └── script_generator.py   # Multi-language script generation
├── web/
│   ├── app.py                # Flask web application
│   └── templates/
│       └── index.html        # Upload form UI
├── assets/                   # Phone mockups, backgrounds, music
├── output/                   # Generated videos
├── uploads/                  # User uploaded wallpapers
├── requirements.txt
└── README.md
```

## 🎬 Video Template Structure

The generated ad video contains exactly **3 scenes**:

### Scene 1: Live Wallpaper Preview (4-6s)
- Displays a phone mockup with the wallpaper inserted inside
- Supports both image and video wallpapers
- Voiceover introduces the wallpaper using the god name
- Auto-loops video wallpapers if needed

### Scene 2: App Showcase (5-7s)
- Shows app interface with multiple wallpaper thumbnails
- Smooth fade transitions
- Voiceover highlights app variety and experience

### Scene 3: Play Store Install (4-6s)
- Displays Play Store listing on phone mockup
- Shows install button and app details
- Localized CTA voiceover based on language

**Total Duration**: ~13-19 seconds (varies based on voiceover length)

## 🔧 Installation

1. **Clone or navigate to the project directory**:
```bash
cd d:\Project\sanatan-app
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import moviepy; print('MoviePy installed successfully')"
```

## 🚀 Usage

### Option 1: Web Interface (Recommended)

1. **Start the Flask server**:
```bash
python web/app.py
```

2. **Open your browser**:
Navigate to `http://localhost:5000`

3. **Fill the form**:
   - **God Name**: e.g., "Lord Shiva"
   - **Custom Text**: e.g., "Feel the divine presence"
   - **Language**: Select English or Hindi
   - **Wallpaper**: Upload image or video file

4. **Generate and Download**:
Click "Generate Ad Video" and wait for processing (1-3 minutes)

### Option 2: Programmatic Usage

```python
from templates.base_template import generate_video

params = {
    'wallpaper': 'path/to/wallpaper.jpg',
    'god_name': 'Lord Shiva',
    'custom_text': 'Feel the divine presence',
    'language_code': 'en'  # or 'hi' for Hindi
}

output_path = generate_video(params)
print(f"Video generated: {output_path}")
```

## 🎙️ Voice Abstraction Architecture

The voice generation system uses a **provider pattern** for easy extensibility:

```python
# Current implementation (gTTS)
from audio.voice_generator import VoiceGenerator, GTTSProvider

generator = VoiceGenerator(provider=GTTSProvider())
audio_path, duration = generator.generate_voiceover(
    text="Experience divine energy",
    language="en",
    output_path="output.mp3"
)
```

### Adding New Voice Providers

To integrate a different TTS service (e.g., ElevenLabs, Azure):

```python
from audio.voice_generator import VoiceProvider

class ElevenLabsProvider(VoiceProvider):
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id
    
    def generate(self, text: str, language: str, output_path: str):
        # Your ElevenLabs API integration
        # Return (audio_path, duration)
        pass

# Use it
from audio.voice_generator import VoiceGenerator
generator = VoiceGenerator(provider=ElevenLabsProvider(api_key="...", voice_id="..."))
```

## 📝 Script Generation

Scripts are automatically generated based on parameters:

**English Example**:
- Scene 1: "Experience divine energy with Lord Shiva live wallpaper. Feel the divine presence"
- Scene 2: "Explore hundreds of divine live wallpapers in our app. Transform your screen with spiritual beauty."
- Scene 3: "Download now from Play Store and bring divine presence to your phone."

**Hindi Example**:
- Scene 1: "भगवान शिव के लाइव वॉलपेपर के साथ दिव्य ऊर्जा का अनुभव करें। दिव्य उपस्थिति महसूस करें"
- Scene 2: "हमारे ऐप में सैकड़ों दिव्य लाइव वॉलपेपर देखें। अपनी स्क्रीन को आध्यात्मिक सुंदरता से सजाएं।"
- Scene 3: "प्ले स्टोर से अभी डाउनलोड करें और अपने फोन में दिव्यता लाएं।"

### Adding New Languages

Edit `scripts/script_generator.py`:

```python
TEMPLATES = {
    'en': { ... },
    'hi': { ... },
    'es': {  # Spanish
        'scene1': "Experimenta energía divina con {god_name} fondo de pantalla. {custom_text}",
        'scene2': "Explora cientos de fondos de pantalla divinos en nuestra aplicación.",
        'scene3': "Descarga ahora desde Play Store."
    }
}
```

## 🎨 Parameter Flow

```
User Input (Web Form)
    ↓
Flask Backend (web/app.py)
    ↓
Base Template (templates/base_template.py)
    ↓
Script Generator → Voice Generator
    ↓
Scene 1 → Scene 2 → Scene 3
    ↓
Concatenate + Background Music
    ↓
Final MP4 Video
```

## ⚙️ Design Decisions & Trade-offs

### 1. **gTTS as Default Voice Provider**
- ✅ **Pros**: Free, no API keys, multi-language, reliable
- ❌ **Cons**: Limited voice customization, requires internet
- **Alternative**: ElevenLabs for premium voices (requires API key)

### 2. **Automatic Placeholder Generation**
- ✅ **Pros**: Works out-of-the-box without manual asset creation
- ❌ **Cons**: Generic appearance
- **Improvement**: Replace with actual app screenshots in `assets/`

### 3. **Fixed 3-Scene Structure**
- ✅ **Pros**: Consistent, predictable, easy to maintain
- ❌ **Cons**: Less flexible for variations
- **Extension**: Add scene variations in separate template files

### 4. **Synchronous Video Generation**
- ✅ **Pros**: Simple, reliable, easy to debug
- ❌ **Cons**: User waits during generation (1-3 min)
- **Improvement**: Add background task queue (Celery) for async processing

### 5. **MoviePy for Video Composition**
- ✅ **Pros**: Python-native, flexible, well-documented
- ❌ **Cons**: Slower than FFmpeg CLI for large videos
- **Alternative**: Direct FFmpeg for production at scale

## 🎯 Extensibility Points

### Adding New Scenes
Create a new scene module in `templates/`:

```python
class Scene4CustomScene:
    def create(self, voiceover_path: str, duration: float):
        # Your scene logic
        return video_clip
```

Update `base_template.py` to include it in the concatenation.

### Custom Transitions
Modify scene modules to add custom transitions:

```python
scene_clip = scene_clip.crossfadein(1.0).crossfadeout(1.0)
```

### Background Music
Add `background_music.mp3` to `assets/` directory. The system will automatically:
- Loop it to match video duration
- Mix at 20% volume with voiceovers

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'moviepy'"
```bash
pip install moviepy==1.0.3
```

### "gTTS error: Connection timeout"
- Check internet connection
- gTTS requires internet to generate speech

### "Video generation takes too long"
- Normal for first run (1-3 minutes)
- Subsequent runs are faster
- Consider using lower resolution for testing

### "Phone mockup not found"
- The system auto-generates a basic phone frame
- For better results, add `assets/phone_mockup.png`

## 📦 Dependencies

- **moviepy**: Video composition and editing
- **Flask**: Web interface
- **gTTS**: Text-to-speech generation
- **Pillow**: Image processing
- **numpy**: Numerical operations

## 🔮 Future Enhancements

1. **Async Processing**: Background task queue for video generation
2. **Premium Voices**: ElevenLabs integration for natural voices
3. **Template Variations**: Multiple scene layouts and styles
4. **Batch Generation**: Generate multiple videos from CSV
5. **Preview Mode**: Quick low-res preview before full render
6. **Analytics**: Track generation metrics and popular configurations

## 📄 License

This project is created for educational and commercial use.

## 👨‍💻 Author

Built by a Senior Python + Video Automation Engineer

---

**Need Help?** Check the code comments or modify the templates to suit your needs!
