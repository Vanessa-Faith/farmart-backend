from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app import db
from app.models.animal import Animal
from app.schemas.animal import animal_schema, animals_schema, animal_update_schema
from app.utils.image_handler import save_animal_image, delete_animal_image
from marshmallow import ValidationError
from sqlalchemy.orm.attributes import flag_modified

animals_bp = Blueprint('animals', __name__)

@animals_bp.route('/api/animals', methods=['GET'])
def get_animals():
    try:
        query = Animal.query.filter_by(status='available')
        
        animal_type = request.args.get('type')
        breed = request.args.get('breed')
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        county = request.args.get('county')
        search = request.args.get('search')
        sort = request.args.get('sort', 'created_at_desc')
        
        if animal_type:
            query = query.filter(Animal.type.ilike(f'%{animal_type}%'))
        if breed:
            query = query.filter(Animal.breed.ilike(f'%{breed}%'))
        if min_age:
            query = query.filter(Animal.age_months >= min_age)
        if max_age:
            query = query.filter(Animal.age_months <= max_age)
        if county:
            query = query.filter(Animal.county.ilike(f'%{county}%'))
        if search:
            query = query.filter(or_(
                Animal.title.ilike(f'%{search}%'),
                Animal.type.ilike(f'%{search}%'),
                Animal.breed.ilike(f'%{search}%')
            ))
        
        if sort == 'price_asc':
            query = query.order_by(Animal.price_per_unit.asc())
        elif sort == 'price_desc':
            query = query.order_by(Animal.price_per_unit.desc())
        elif sort == 'age_asc':
            query = query.order_by(Animal.age_months.asc())
        elif sort == 'age_desc':
            query = query.order_by(Animal.age_months.desc())
        else:
            query = query.order_by(Animal.created_at.desc())
        
        animals = query.all()
        return jsonify(animals_schema.dump(animals)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch animals'}), 500

@animals_bp.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return jsonify(animal_schema.dump(animal)), 200

@animals_bp.route('/api/animals', methods=['POST'])
@jwt_required()
def create_animal():
    try:
        farmer_id = get_jwt_identity()
        data = request.get_json()
        
        images = data.pop('images', [])
        validated_data = animal_schema.load(data)
        validated_data['farmer_id'] = farmer_id
        validated_data['images'] = images
        
        animal = Animal(**validated_data)
        db.session.add(animal)
        db.session.commit()
        
        return jsonify(animal_schema.dump(animal)), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create animal'}), 500

@animals_bp.route('/api/animals/<int:animal_id>', methods=['PUT'])
@jwt_required()
def update_animal(animal_id):
    try:
        farmer_id = get_jwt_identity()
        animal = Animal.query.filter_by(id=animal_id, farmer_id=farmer_id).first_or_404()
        
        data = request.get_json()
        images = data.pop('images', None)
        validated_data = animal_update_schema.load(data)
        
        for key, value in validated_data.items():
            setattr(animal, key, value)
        
        if images is not None:
            animal.images = images
            flag_modified(animal, 'images')
        
        db.session.commit()
        return jsonify(animal_schema.dump(animal)), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update animal'}), 500

@animals_bp.route('/api/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required()
def delete_animal(animal_id):
    try:
        farmer_id = get_jwt_identity()
        animal = Animal.query.filter_by(id=animal_id, farmer_id=farmer_id).first_or_404()
        
        for image_path in animal.images or []:
            delete_animal_image(image_path)
        
        db.session.delete(animal)
        db.session.commit()
        
        return jsonify({'message': 'Animal deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete animal'}), 500

@animals_bp.route('/api/animals/<int:animal_id>/upload-image', methods=['POST'])
@jwt_required()
def upload_animal_image(animal_id):
    try:
        farmer_id = get_jwt_identity()
        animal = Animal.query.filter_by(id=animal_id, farmer_id=farmer_id).first_or_404()
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        image_path = save_animal_image(file, animal_id)
        if not image_path:
            return jsonify({'error': 'Failed to save image'}), 400
        
        if not animal.images:
            animal.images = []
        
        current_images = list(animal.images)
        current_images.append(image_path)
        animal.images = current_images
        flag_modified(animal, 'images')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'image_path': image_path,
            'animal': animal_schema.dump(animal)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload image'}), 500

@animals_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)