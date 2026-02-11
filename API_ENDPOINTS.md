# FarmArt Backend API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## Authentication Endpoints

### Register User
**POST** `/api/auth/register`

Register a new user (farmer or buyer).

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "buyer"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "buyer",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

---

### Login
**POST** `/api/auth/login`

Login and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "buyer",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

---

### Get Current User
**GET** `/api/auth/me`

Get current authenticated user details.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "buyer",
  "created_at": "2024-01-01T10:00:00"
}
```

---

## Animal Endpoints

### List All Animals
**GET** `/api/animals`

Get all available animals with optional filters.

**Query Parameters:**
- `type` or `animal_type` - Filter by animal type
- `breed` - Filter by breed
- `title`, `search`, or `q` - Search by title
- `min_age`, `max_age` - Filter by age range
- `min_price`, `max_price` - Filter by price range
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20)

**Example:**
```
GET /api/animals?type=cow&min_price=5000&max_price=20000
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "farmer_id": 2,
    "title": "Healthy Dairy Cow",
    "animal_type": "cow",
    "breed": "Holstein",
    "age": 3,
    "price": 15000.00,
    "quantity": 5,
    "description": "High milk production",
    "status": "available",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
]
```

---

### Get Single Animal
**GET** `/api/animals/<id>`

Get details of a specific animal.

**Response:** `200 OK`
```json
{
  "id": 1,
  "farmer_id": 2,
  "title": "Healthy Dairy Cow",
  "animal_type": "cow",
  "breed": "Holstein",
  "age": 3,
  "price": 15000.00,
  "quantity": 5,
  "description": "High milk production",
  "status": "available",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

### Create Animal
**POST** `/api/animals`

Create a new animal listing (farmers only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Healthy Dairy Cow",
  "animal_type": "cow",
  "breed": "Holstein",
  "age": 3,
  "price": 15000.00,
  "quantity": 5,
  "description": "High milk production"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "farmer_id": 2,
  "title": "Healthy Dairy Cow",
  "animal_type": "cow",
  "breed": "Holstein",
  "age": 3,
  "price": 15000.00,
  "quantity": 5,
  "description": "High milk production",
  "status": "available",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

### Update Animal
**PUT** `/api/animals/<id>`

Update animal listing (owner only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "price": 16000.00,
  "quantity": 4,
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "farmer_id": 2,
  "title": "Healthy Dairy Cow",
  "animal_type": "cow",
  "breed": "Holstein",
  "age": 3,
  "price": 16000.00,
  "quantity": 4,
  "description": "Updated description",
  "status": "available",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

---

### Delete Animal
**DELETE** `/api/animals/<id>`

Delete animal listing (owner only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Animal deleted successfully"
}
```

---

## Cart Endpoints

### Get Cart
**GET** `/api/carts`

Get current user's cart.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "buyer_id": 1,
  "items": [
    {
      "id": 1,
      "cart_id": 1,
      "animal_id": 1,
      "animal": {
        "id": 1,
        "title": "Healthy Dairy Cow",
        "price": 15000.00
      },
      "quantity": 2,
      "added_at": "2024-01-01T10:00:00"
    }
  ],
  "total": 30000.00,
  "created_at": "2024-01-01T10:00:00"
}
```

---

### Add to Cart
**POST** `/api/carts/items`

Add item to cart (buyers only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "animal_id": 1,
  "quantity": 2
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "buyer_id": 1,
  "items": [...],
  "total": 30000.00,
  "created_at": "2024-01-01T10:00:00"
}
```

---

### Update Cart Item
**PUT** `/api/carts/items/<item_id>`

Update cart item quantity.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "cart_id": 1,
  "animal_id": 1,
  "animal": {...},
  "quantity": 3,
  "added_at": "2024-01-01T10:00:00"
}
```

---

### Remove from Cart
**DELETE** `/api/carts/items/<item_id>`

Remove item from cart.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Item removed from cart"
}
```

---

## Order Endpoints

### Get Orders
**GET** `/api/orders`

Get user's orders. Buyers see their purchases, farmers see orders for their animals.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "buyer_id": 1,
    "total_amount": 30000.00,
    "status": "pending",
    "items": [
      {
        "id": 1,
        "order_id": 1,
        "animal_id": 1,
        "animal": {...},
        "farmer_id": 2,
        "quantity": 2,
        "unit_price": 15000.00,
        "subtotal": 30000.00
      }
    ],
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
]
```

---

### Get Single Order
**GET** `/api/orders/<id>`

Get details of a specific order.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "buyer_id": 1,
  "total_amount": 30000.00,
  "status": "pending",
  "items": [...],
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

### Create Order
**POST** `/api/orders`

Create order from cart (buyers only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `201 Created`
```json
{
  "id": 1,
  "buyer_id": 1,
  "total_amount": 30000.00,
  "status": "pending",
  "items": [...],
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

### Pay for Order
**POST** `/api/orders/<id>/pay`

Process payment for order (buyers only).

**Headers:** `Authorization: Bearer <token>`

**Request Body (optional):**
```json
{
  "provider": "mpesa",
  "provider_transaction_id": "ABC123XYZ"
}
```

**Response:** `200 OK`
```json
{
  "message": "Payment processed",
  "payment": {
    "id": 1,
    "order_id": 1,
    "amount": 30000.00,
    "provider": "mpesa",
    "provider_transaction_id": "ABC123XYZ",
    "status": "succeeded",
    "created_at": "2024-01-01T10:00:00"
  },
  "order": {...}
}
```

---

### Confirm Order
**POST** `/api/orders/<id>/confirm`

Farmer confirms order (farmers only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Order confirmed",
  "order": {...}
}
```

---

### Reject Order
**POST** `/api/orders/<id>/reject`

Farmer rejects order (farmers only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Order rejected",
  "order": {...}
}
```

---

### Update Order Status
**PUT** `/api/orders/<id>`

Update order status (farmers only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Response:** `200 OK`
```json
{
  "message": "Order confirmed",
  "order": {...}
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "message": "Descriptive error message"
}
```

### 401 Unauthorized
```json
{
  "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "message": "Access denied"
}
```

### 404 Not Found
```json
{
  "message": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "message": "Invalid token identity"
}
```

### 500 Internal Server Error
```json
{
  "message": "Internal server error"
}
```

---

## Order Status Flow

1. **pending** - Order created, awaiting payment
2. **paid** - Payment processed by buyer
3. **confirmed** - Order confirmed by farmer
4. **rejected** - Order rejected by farmer

---

## Testing with cURL

### Register a Farmer
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Farmer John",
    "email": "farmer@example.com",
    "password": "password123",
    "role": "farmer"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "password123"
  }'
```

### Create Animal (use token from login)
```bash
curl -X POST http://localhost:5000/api/animals \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Healthy Dairy Cow",
    "animal_type": "cow",
    "breed": "Holstein",
    "age": 3,
    "price": 15000,
    "quantity": 5,
    "description": "High milk production"
  }'
```

### Get All Animals
```bash
curl http://localhost:5000/api/animals
```
