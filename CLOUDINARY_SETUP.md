# Cloudinary Image Upload Setup

## Installation

```bash
# Activate virtual environment first
source venv/bin/activate

# Install cloudinary
pip install cloudinary==1.36.0
```

## Configuration

1. Sign up for free Cloudinary account at https://cloudinary.com/users/register/free

2. Get your credentials from Cloudinary Dashboard

3. Add to `.env` file:
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Usage

### Create Animal with Image (multipart/form-data)

```bash
curl -X POST http://localhost:5000/api/animals \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=Healthy Cow" \
  -F "animal_type=Cow" \
  -F "breed=Holstein" \
  -F "age=3" \
  -F "price=45000" \
  -F "quantity=5" \
  -F "description=High milk production" \
  -F "image=@/path/to/image.jpg"
```

### Update Animal with Image

```bash
curl -X PUT http://localhost:5000/api/animals/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "price=50000" \
  -F "image=@/path/to/new-image.jpg"
```

### JavaScript/Frontend Example

```javascript
const formData = new FormData();
formData.append('title', 'Healthy Cow');
formData.append('animal_type', 'Cow');
formData.append('breed', 'Holstein');
formData.append('age', 3);
formData.append('price', 45000);
formData.append('quantity', 5);
formData.append('description', 'High milk production');
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/api/animals', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

## Features

- Automatic image upload to Cloudinary
- Image deletion when animal is deleted
- Image replacement when updating
- Supported formats: PNG, JPG, JPEG, GIF, WEBP
- Images stored in `farmart/animals` folder on Cloudinary
- Secure HTTPS URLs returned

## Database Changes

Added `image_url` column to `animals` table:
```sql
ALTER TABLE animals ADD COLUMN image_url VARCHAR(500);
```

This will be created automatically when you restart the app.
