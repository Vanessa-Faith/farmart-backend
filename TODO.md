# Farmart Backend Review - TODO List

## Issues Found & Fixes Applied

### ✅ FIXED: add_sample_data.py field mismatch
- Changed `type` → `animal_type`
- Changed `age_months` → `age`
- Changed `price_per_unit` → `price`
- Changed `quantity_available` → `quantity`
- Removed non-existent fields (`first_name`, `last_name`, `user_type`, `phone`, `county`)
- Added `description` field where missing

---

## Remaining Issues to Address

### 1. ⚠️ Missing Cloudinary Configuration
**Status**: Pending setup
**Action Required**: Add Cloudinary credentials to `.env` file:
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Impact**: Image uploads will fail without credentials.

### 2. ⚠️ User Model Missing Fields
**Status**: Design decision needed
**Fields mentioned in pitch but missing in model**:
- `phone` - Contact field
- `county` - Location field
- `first_name`/`last_name` (currently single `name` field)

**Options**:
A. Keep current model (simple `name` field)
B. Expand User model to add `phone` and `county` fields

### 3. ⚠️ add_images.py script exists but not verified
**Status**: Needs testing
**Location**: `add_images.py` - Should add sample images to existing animals

---

## Setup Steps to Get Images Working

### Step 1: Create `.env` file
```env
# Database
DATABASE_URL=sqlite:///instance/farmart_dev.db

# JWT
JWT_SECRET_KEY=dev-secret-key-change-in-production

# Cloudinary (REQUIRED for images)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# M-Pesa (optional)
MPESA_ENV=sandbox
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
```

### Step 2: Initialize database
```bash
python init_db.py
# OR
python -c "from app import create_app; app = create_app(); from app.models.models import db; db.create_all(app=app)"
```

### Step 3: Add sample data
```bash
python add_sample_data.py
```

### Step 4: Run the server
```bash
python app.py
```

### Step 5: Test image upload
```bash
curl -X POST http://localhost:5000/api/animals \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=New Cow" \
  -F "animal_type=Cow" \
  -F "price=1000" \
  -F "image=@/path/to/image.jpg"
```

---

## Backend Components Status

| Component | Status | Notes |
|-----------|--------|-------|
| Auth (Login/Register) | ✅ Working | JWT-based |
| User Management | ✅ Working | Basic fields only |
| Animals CRUD | ✅ Working | Full CRUD + search/filter |
| Image Upload | ⚠️ Needs config | Cloudinary setup required |
| Cart System | ✅ Working | Full functionality |
| Order System | ✅ Working | With M-Pesa mock |
| Tests | ✅ Setup | Pytest fixtures ready |
| Documentation | ✅ Complete | README + CLOUDINARY_SETUP.md |

---

## Image Integration Flow

```
Frontend (React/Redux)
    ↓ FormData with image
Backend API (/api/animals POST)
    ↓ cloudinary_helper.upload_image()
Cloudinary CDN
    ↓ Returns secure_url
Database (image_url column)
    ↓
Frontend displays: <img src={animal.image_url} />
```

