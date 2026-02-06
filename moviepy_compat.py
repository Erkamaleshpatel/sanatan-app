"""
Compatibility patch for MoviePy 1.0.3 with Pillow 10+
This fixes the Image.ANTIALIAS deprecation issue.
"""

from PIL import Image

# Add ANTIALIAS back for compatibility with MoviePy 1.0.3
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
    print("[OK] Applied MoviePy compatibility patch for Pillow 10+")
