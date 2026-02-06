"""
Flask web application for ad video generation.
Provides a simple UI for uploading wallpapers and generating videos.
"""

from flask import Flask, render_template, request, send_file, jsonify, url_for
import os
import sys
from werkzeug.utils import secure_filename

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    # Get absolute path to output directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, app.config['OUTPUT_FOLDER'])
    file_path = os.path.join(output_dir, filename)
    
    print(f"Download request for: {filename}")
    print(f"Looking for file at: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, mimetype='video/mp4')
    else:
        return jsonify({'error': f'File not found: {filename}'}), 404


if __name__ == '__main__':
    print("Starting Live Wallpaper Ad Generator...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
