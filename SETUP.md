# 🚀 Quick Setup Guide - Live Wallpaper Ad Generator

## ⚠️ Important: Python Version Compatibility

**This project works best with Python 3.10 or 3.11** due to MoviePy 1.0.3 dependency compatibility.

If you're using **Python 3.13**, there's a known compatibility issue between MoviePy 1.0.3 and newer Pillow versions.

## 📋 Installation Steps

### Option 1: Recommended (Python 3.10/3.11)

```bash
# 1. Navigate to project
cd d:\Project\sanatan-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test the system
python test_generation.py

# 4. Run web interface
python web/app.py
```

### Option 2: Python 3.13 Workaround

If you must use Python 3.13, install a pre-built Pillow wheel:

```bash
# Install dependencies one by one
pip install moviepy==1.0.3
pip install Flask==3.0.0
pip install gTTS==2.5.4
pip install numpy==1.26.4
pip install pydub==0.25.1

# Download and install compatible Pillow wheel
# Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
# Or use:
pip install --only-binary=:all: Pillow==10.2.0

# Test
python test_generation.py
```

## ✅ Verify Installation

Run this to check if everything is installed:

```bash
python -c "import moviepy; import gtts; from PIL import Image; print('✓ All dependencies installed!')"
```

## 🎬 Usage

### Web Interface
```bash
python web/app.py
# Open: http://localhost:5000
```

### Programmatic
```python
from templates.base_template import generate_video

params = {
    'wallpaper': 'assets/sample_wallpaper.jpg',
    'god_name': 'Lord Shiva',
    'custom_text': 'Feel the divine presence',
    'language_code': 'en'
}

output = generate_video(params)
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'gtts'"
```bash
pip install gTTS
```

### "AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'"
This means you have Pillow 11+ with MoviePy 1.0.3. Solutions:
1. Use Python 3.10 or 3.11 (recommended)
2. Downgrade Pillow: `pip install Pillow==10.2.0 --only-binary=:all:`

### "Video generation is slow"
- Normal: First video takes 1-3 minutes
- Includes: Script generation, voiceover synthesis, video rendering

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Need Help?** The system is fully functional - dependency installation is the only potential hurdle!
