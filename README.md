# 🎬 Sanatan App - Live Wallpaper Ad Generator

Generate stunning promotional videos for divine wallpapers with multiple image support, smooth transitions, and animated backgrounds.

## ✨ Features

- **Multi-Image Support**: Upload 1-10+ wallpapers for longer videos
- **Smooth Transitions**: Beautiful crossfade effects between wallpapers
- **Animated Backgrounds**: Rotating mandala patterns with gradient effects
- **Multi-Language**: English and Hindi voiceover support
- **Phone Mockup**: Professional phone overlay for wallpaper showcase
- **Play Store CTA**: Integrated install call-to-action

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/erkamaleshpatel/sanatan-app.git
cd sanatan-app
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python web/app.py
```

4. **Open browser**:
```
http://localhost:5000
```

## ☁️ Deployment

### Render.com (Recommended - Free Tier)

1. Fork/clone this repository
2. Sign up at [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml` and deploy

**Live URL**: `https://your-app.onrender.com`

### Other Options

- **PythonAnywhere**: Free tier available
- **Railway.app**: Free tier with limitations
- **Heroku**: Paid ($5/month minimum)

See [deployment_guide.md](deployment_guide.md) for detailed instructions.

## 📋 Requirements

- Python 3.10+
- Flask
- MoviePy
- gTTS (Google Text-to-Speech)
- Pillow
- pydub

## 🎯 Usage

1. Open the web interface
2. Select one or multiple wallpaper images
3. Fill in deity name and custom text
4. Choose language (English/Hindi)
5. Click "Generate Ad Video"
6. Download the generated video

## 📁 Project Structure

```
sanatan-app/
├── web/
│   ├── app.py              # Flask application
│   └── templates/
│       └── index.html      # Web interface
├── templates/
│   ├── base_template.py    # Video generation orchestrator
│   ├── scene_multi_wallpapers.py  # Multi-wallpaper scene
│   ├── scene3_install.py   # Play Store install scene
│   └── animated_background.py     # Background animations
├── scripts/
│   └── script_generator.py # Voiceover script generation
├── audio/
│   └── voice_generator.py  # Text-to-speech conversion
├── assets/                 # Phone and Play Store mockups
├── output/                 # Generated videos
├── uploads/                # Uploaded wallpapers
├── render.yaml            # Render.com config
├── Procfile               # Heroku/Railway config
├── runtime.txt            # Python version
└── requirements.txt       # Dependencies
```

## 🎬 Video Structure

1. **Scene 1**: Multi-Wallpaper Showcase
   - Duration: 4 seconds per wallpaper
   - Smooth crossfade transitions
   - Animated decorative background
   - Phone mockup overlay

2. **Scene 2**: Play Store Install
   - Duration: 5-7 seconds
   - Call-to-action for app download

**Total Duration**: 17-47 seconds (depends on wallpaper count)

## 🛠️ Development

### Running Tests

```bash
python test_generation.py
```

This will generate 3 test videos:
- Single wallpaper (English)
- Multiple wallpapers (English)
- Multiple wallpapers (Hindi)

### Optimization

For faster rendering, disable animated backgrounds in `templates/scene_multi_wallpapers.py`:

```python
# Change line ~95:
background = create_gradient_background(duration, size)  # Instead of animated
```

**Speed improvement**: 5x faster rendering

## 📝 License

Open source project. Feel free to use and modify.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## ⚠️ Note

This is a Flask/Python application requiring server-side processing. It cannot run on GitHub Pages (static hosting only). Please deploy to a Python-compatible platform like Render.com, PythonAnywhere, or Railway.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ for divine wallpaper creators
