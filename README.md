# Farmart Backend - Feature 2: Animal Listings & CRUD

Backend implementation for animal listings with search, filtering, and CRUD operations.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
1. Create PostgreSQL database:
```sql
CREATE DATABASE farmart_db;
```

2. Update `.env` file with your database credentials:
```
DATABASE_URL=postgresql://your_username:your_password@localhost/farmart_db
JWT_SECRET_KEY=your-secret-key-here
```

3. Initialize database:
```bash
python init_db.py
```

### 3. Run the Application
```bash
python run.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Public Endpoints

#### GET /api/animals
Get all available animals with optional filtering and search.

**Query Parameters:**
- `type` - Filter by animal type (cow, pig, chicken, etc.)
- `breed` - Filter by breed
- `min_age` - Minimum age in months
- `max_age` - Maximum age in months  
- `county` - Filter by county
- `search` - Search in title, type, and breed
- `sort` - Sort order: `price_asc`, `price_desc`, `age_asc`, `age_desc`, `created_at_desc` (default)

**Example:**
```
GET /api/animals?type=cow&min_age=12&sort=price_asc
```

#### GET /api/animals/:id
Get single animal by ID.

### Farmer Endpoints (Require JWT Authentication)

#### POST /api/animals
Create new animal listing.

**Request Body:**
```json
{
  "title": "Premium Dairy Cow",
  "type": "cow",
  "breed": "Holstein",
  "age_months": 24,
  "price_per_unit": 1500.00,
  "quantity_available": 1,
  "county": "Nairobi"
}
```

#### PUT /api/animals/:id
Update existing animal (farmer can only update their own animals).

#### DELETE /api/animals/:id
Delete animal (farmer can only delete their own animals).

#### POST /api/animals/:id/upload-image
Upload image for animal.

**Form Data:**
- `image` - Image file (PNG, JPG, JPEG, GIF, max 5MB)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/
│   │   ├── animal.py        # Animal model
│   │   └── user.py          # User model
│   ├── routes/
│   │   └── animals.py       # Animal routes
│   ├── schemas/
│   │   └── animal.py        # Marshmallow schemas
│   └── utils/
│       └── image_handler.py # Image upload utilities
├── uploads/
│   └── animals/             # Uploaded animal images
├── run.py                   # Application entry point
├── init_db.py              # Database initialization
├── test_api.py             # API testing script
└── requirements.txt        # Dependencies
```

## Testing

Run the test script to verify API endpoints:
```bash
python test_api.py
```

## Notes

- Images are automatically resized to 800x600 max while maintaining aspect ratio
- All uploaded images are stored in `uploads/animals/{animal_id}/` directory
- JWT authentication is required for farmer endpoints (you'll need to implement auth first)
- The Animal model includes a relationship with User model (farmer)