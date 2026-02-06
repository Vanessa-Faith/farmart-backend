import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

def save_animal_image(file, animal_id):
    if not file or not allowed_file(file.filename):
        return None
    
    filename = generate_unique_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    animal_folder = os.path.join(upload_folder, 'animals', str(animal_id))
    os.makedirs(animal_folder, exist_ok=True)
    
    filepath = os.path.join(animal_folder, filename)
    
    try:
        image = Image.open(file)
        image.thumbnail((800, 600), Image.Resampling.LANCZOS)
        image.save(filepath, optimize=True, quality=85)
        
        return f"animals/{animal_id}/{filename}"
    except Exception as e:
        return None

def delete_animal_image(image_path):
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except:
        return False