#  Quick Start Guide

## Start the Backend in 3 Steps

### 1️⃣ Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2️⃣ Run the Server
```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 3️⃣ Test It Works
Open a new terminal and run:
```bash
curl http://localhost:5000/api/animals
```

You should get: `[]` (empty array - no animals yet)

---

##  Quick Test Flow

### 1. Register a Farmer
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Farmer",
    "email": "farmer@test.com",
    "password": "password123",
    "role": "farmer"
  }'
```

### 2. Login as Farmer
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@test.com",
    "password": "password123"
  }'
```

**Copy the `access_token` from the response!**

### 3. Create an Animal
```bash
curl -X POST http://localhost:5000/api/animals \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Healthy Cow",
    "animal_type": "cow",
    "breed": "Holstein",
    "age": 3,
    "price": 15000,
    "quantity": 5,
    "description": "Great milk producer"
  }'
```

### 4. View All Animals
```bash
curl http://localhost:5000/api/animals
```

---

##  For Frontend Developers

### Base URL
```
http://localhost:5000/api
```

### Authentication Header
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### Example: Fetch Animals (JavaScript)
```javascript
fetch('http://localhost:5000/api/animals')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Example: Login (JavaScript)
```javascript
fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})
  .then(res => res.json())
  .then(data => {
    const token = data.access_token;
    const user = data.user;
    // Store token for future requests
  });
```

### Example: Create Animal (JavaScript)
```javascript
fetch('http://localhost:5000/api/animals', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Healthy Cow',
    animal_type: 'cow',
    breed: 'Holstein',
    age: 3,
    price: 15000,
    quantity: 5,
    description: 'Great milk producer'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

##  Complete User Flow

### Buyer Journey
1. Register as buyer → `POST /api/auth/register`
2. Login → `POST /api/auth/login`
3. Browse animals → `GET /api/animals`
4. Add to cart → `POST /api/carts/items`
5. View cart → `GET /api/carts`
6. Create order → `POST /api/orders`
7. Pay for order → `POST /api/orders/{id}/pay`

### Farmer Journey
1. Register as farmer → `POST /api/auth/register`
2. Login → `POST /api/auth/login`
3. Create animal listing → `POST /api/animals`
4. View orders → `GET /api/orders`
5. Confirm/reject orders → `POST /api/orders/{id}/confirm` or `/reject`

---

##  Full Documentation

- **API_ENDPOINTS.md** - Complete API reference
- **IMPLEMENTATION_SUMMARY.md** - What's implemented
- **README.md** - Project overview

---

##  Need Help?

**Server won't start?**
- Check if port 5000 is available
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**Database errors?**
- Delete `instance/farmart_dev.db` and restart

**Import errors?**
- Activate virtual environment: `source venv/bin/activate`

---

**Happy Coding! **
