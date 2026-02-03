# Farmart Backend API

E-commerce platform connecting farmers directly with buyers to eliminate middlemen.

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and update DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY
```

### 2. Setup Database

```bash
# Start PostgreSQL with Docker
docker run --name farmart-db \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_USER=dev \
  -e POSTGRES_DB=farmart \
  -p 5432:5432 \
  -d postgres:15

# Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Run the Application

```bash
python run.py
```

API runs at `http://localhost:5000`

Test health endpoint: `curl http://localhost:5000/api/health`

## Project Structure

```
farmart-backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   │   ├── user.py         # User (farmers & buyers)
│   │   ├── animal.py       # Animal listings
│   │   ├── cart.py         # Cart & CartItem
│   │   ├── order.py        # Order & OrderItem
│   │   └── payment.py      # Payment records
│   └── routes/              # API endpoints
│       ├── auth.py         # Register, login, JWT
│       ├── animals.py      # CRUD animals, search, filter
│       ├── carts.py        # Cart management
│       └── orders.py       # Orders, confirm/reject, payment
├── db/
│   └── schema.dbml         # Database schema for dbdiagram.io
├── config.py               # Configuration
├── run.py                  # Entry point
├── requirements.txt        # Dependencies
└── .env.example           # Environment template
```

## API Endpoints

### Auth (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and get JWT token
- `GET /me` - Get current user (protected)

### Animals (`/api/animals`)
- `GET /` - List all animals (with filters)
- `GET /:id` - Get animal details
- `POST /` - Create animal (farmer only)
- `PUT /:id` - Update animal (owner only)
- `DELETE /:id` - Delete animal (owner only)

### Cart (`/api/carts`)
- `GET /` - Get current cart
- `POST /items` - Add item to cart
- `PUT /items/:id` - Update cart item
- `DELETE /items/:id` - Remove from cart

### Orders (`/api/orders`)
- `GET /` - Get user's orders
- `GET /:id` - Get order details
- `POST /` - Create order from cart
- `POST /:id/confirm` - Farmer confirms order
- `POST /:id/reject` - Farmer rejects order
- `POST /:id/pay` - Process payment

## Feature-Based Development (Team Workflow)

Each team member owns ONE feature end-to-end (backend + frontend):

### Features Assignment:
1. **Authentication** - Team Lead (Vanessa) - 🧪 IN TESTING
   - Backend: Register/Login with validation (implemented, needs testing)
   - Frontend: Redux auth, Login/Register forms, JWT handling (implemented, needs testing)
   
2. **Animals Listings** - Assign to team member
   - Backend: CRUD endpoints with search/filter
   - Frontend: Animal list page, detail page, create/edit forms (farmers)
   
3. **Shopping Cart** - Assign to team member
   - Backend: Add/update/remove cart items
   - Frontend: Cart page, add-to-cart buttons, quantity controls
   
4. **Orders & Payment** - Assign to team member
   - Backend: Create order, farmer confirm/reject, payment integration
   - Frontend: Checkout flow, order history, farmer order management
   
5. **QA & Testing** - Assign to team member
   - Write Cypress E2E tests for all features
   - Manual testing and bug reporting
   - Test data creation

### Development Workflow:
1. Each person creates a feature branch: `git checkout -b feature/animals`
2. Implement both backend AND frontend for your feature
3. Test your feature end-to-end locally
4. Create PR when complete
5. Team reviews PR within 24 hours
6. Merge to dev branch

### Daily Standups (15 min):
- What did you complete yesterday?
- What are you working on today?
- Any blockers?

## Sprint Timeline (2 weeks - Jan 27 to Feb 10, 2026)

**Days 1-3**: Auth (DONE ✅) + Animals feature kickoff  
**Days 4-7**: Animals complete + Cart feature  
**Days 8-11**: Orders/Payment + E2E testing  
**Days 12-13**: Bug fixes + polish  
**Day 14**: Demo rehearsal

## Notes

- **Auth is COMPLETE** - backend validation + frontend Redux working
- Routes with `# TODO:` are skeleton structure for team members
- Models are complete and match the DBML schema
- JWT authentication configured and tested
- CORS enabled for frontend (http://localhost:5173 for Vite)
- Use `@jwt_required()` decorator for protected routes
- Get current user ID with `get_jwt_identity()`
- Frontend runs on Vite (port 5173), backend on Flask (port 5000)

---

**Database Schema**: View on dbdiagram.io (link from team lead)
