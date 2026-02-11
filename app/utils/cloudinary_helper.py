import cloudinary
import cloudinary.uploader
import os
from werkzeug.utils import secure_filename

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file):
    """Upload image to Cloudinary and return URL"""
    if not file or not allowed_file(file.filename):
        return None, "Invalid file type"
    
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="farmart/animals",
            resource_type="image"
        )
        return result['secure_url'], None
    except Exception as e:
        return None, str(e)

def delete_image(image_url):
    """Delete image from Cloudinary"""
    try:
        public_id = image_url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(f"farmart/animals/{public_id}")
        return True
    except:
        return False
