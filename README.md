# FarmArt Backend

A robust Flask-based backend API for livestock trading and order management.

## Tech Stack

- **Web Framework**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Database**: SQLite/PostgreSQL
- **Runtime**: Python 3.8+

## Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd farmart-backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**
   Create `.env` file with:
   ```bash
   DATABASE_URL=sqlite:///instance/farmart_dev.db
   MPESA_CONSUMER_KEY=your_key
   MPESA_CONSUMER_SECRET=your_secret
   MPESA_ENV=sandbox
   MPESA_SHORTCODE=174379
   MPESA_PASSKEY=your_passkey
   MPESA_CALLBACK_URL=https://your-domain.com/api/orders/mpesa/callback
   ```

4. **Initialize database**
   ```bash
   python -c "from app import create_app; app = create_app(); from app.models.models import db; db.create_all(app=app)"
   ```

5. **Run application**
   ```bash
   python app.py
   ```

## API Endpoints

### Authentication Required
All endpoints require JWT token:
```
Authorization: Bearer <your-jwt-token>
```

### Order Management
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get specific order
- `POST /api/orders` - Create new order (buyers only)
- `POST /api/orders/<id>/pay` - Initiate M-Pesa payment
- `POST /api/orders/<id>/confirm` - Confirm order (farmers only)
- `POST /api/orders/<id>/reject` - Reject order (farmers only)

### M-Pesa Callback
- `POST /api/orders/mpesa/callback` - Handle payment callbacks

## Database Schema

### Core Models
- **User**: Buyers and farmers with role-based access
- **Animal**: Livestock catalog with pricing and availability
- **Order**: Purchase orders with M-Pesa integration
- **OrderItem**: Items within orders

## Configuration

### Environment Variables
- `FLASK_ENV`: Application environment
- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: JWT signing key
- `MPESA_*`: M-Pesa Daraja API configuration

## Order Lifecycle

1. **Order Created** → **Pending Payment** → **Paid** → **Confirmed**
2. **Order Created** → **Pending Payment** → **Rejected**

## License

MIT License

---

**Made with ❤️ for the farming community**
