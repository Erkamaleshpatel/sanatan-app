"""
Flask web application for ad video generation.
Provides a simple UI for uploading wallpapers and generating videos.
"""

import os
import sys

# Add parent directory to path FIRST
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Apply MoviePy compatibility patch BEFORE any other imports
try:
    import moviepy_compat
except ImportError:
    pass  # Compatibility patch not found, continue anyway

from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename

from templates.base_template import generate_video

# Get base directory (parent of web/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(BASE_DIR, 'output')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main upload form."""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'App is running!'})


@app.route('/generate', methods=['POST'])
def generate():
    """Handle video generation request."""
    try:
        # Support both single and multiple file uploads
        wallpaper_paths = []
        
        # Check for multiple files (new feature)
        if 'wallpapers' in request.files:
            files = request.files.getlist('wallpapers')
            if not files or all(f.filename == '' for f in files):
                return jsonify({'error': 'No wallpaper files selected'}), 400
            
            for file in files:
                if file and file.filename != '':
                    if not allowed_file(file.filename):
                        return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
                    
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    wallpaper_paths.append(filepath)
        
        # Fallback to single file upload (backward compatibility)
        elif 'wallpaper' in request.files:
            file = request.files['wallpaper']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            wallpaper_paths.append(filepath)
        else:
            return jsonify({'error': 'No wallpaper file(s) uploaded'}), 400
        
        if not wallpaper_paths:
            return jsonify({'error': 'No valid wallpaper files uploaded'}), 400
        
        # Get form data
        god_name = request.form.get('god_name', '').strip()
        custom_text = request.form.get('custom_text', '').strip()
        language_code = request.form.get('language_code', 'en').strip()
        
        if not god_name:
            return jsonify({'error': 'God name is required'}), 400
        
        # Prepare parameters
        params = {
            'wallpapers': wallpaper_paths,  # Use list for multi-wallpaper support
            'god_name': god_name,
            'custom_text': custom_text or '',
            'language_code': language_code
        }
        
        # Generate video
        print(f"\nGenerating video with {len(wallpaper_paths)} wallpaper(s)...")
        output_path = generate_video(params)
        
        # Get filename for download
        filename = os.path.basename(output_path)
        download_url = url_for('download', filename=filename)
        
        return jsonify({
            'success': True,
            'message': f'Video generated successfully with {len(wallpaper_paths)} wallpaper(s)!',
            'download_url': download_url,
            'filename': filename
        })
    
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate video: {str(e)}'}), 500


@app.route('/download/<filename>')
def download(filename):
    """Serve generated video for download."""
    try:
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment variable (for cloud hosting) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    
    # Determine if running in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("\n" + "="*60)
    print("[OK] Applied MoviePy compatibility patch for Pillow 10+")
    print("Starting Live Wallpaper Ad Generator...")
    print(f"Environment: {'Development' if debug_mode else 'Production'}")
    print(f"Open your browser and navigate to: http://localhost:{port}")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',  # Allow external connections (required for cloud hosting)
        port=port,
        debug=debug_mode
    )
