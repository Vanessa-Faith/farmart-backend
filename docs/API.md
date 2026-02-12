# Farmart API Reference (Frontend)

Base URL (dev): `http://localhost:5000/api`

## Auth
- `POST /auth/register`
  - Body: `{ "name": "", "email": "", "password": "", "role": "farmer|buyer" }`
  - Response: `{ message, user }`
- `POST /auth/login`
  - Body: `{ "email": "", "password": "" }`
  - Response: `{ access_token, user }`
- `GET /auth/me` (requires JWT)
  - Header: `Authorization: Bearer <token>`
  - Response: user

## Animals
- `GET /animals`
  - Query: `?type=&breed=&min_age=&max_age=&min_price=&max_price=` (to be implemented)
- `GET /animals/:id`
- `POST /animals` (farmer only, JWT)
- `PUT /animals/:id` (owner only, JWT)
- `DELETE /animals/:id` (owner only, JWT)

## Cart
- `GET /carts` (JWT)
- `POST /carts/items` (JWT)
  - Body: `{ "animal_id": 1, "quantity": 2 }`
- `PUT /carts/items/:id` (JWT)
  - Body: `{ "quantity": 3 }`
- `DELETE /carts/items/:id` (JWT)

## Orders
- `GET /orders` (JWT)
- `GET /orders/:id` (JWT)
- `POST /orders` (JWT) — create order from cart
- `POST /orders/:id/confirm` (farmer only, JWT)
- `POST /orders/:id/reject` (farmer only, JWT)
- `POST /orders/:id/pay` (JWT)

## Notes
- All protected endpoints require `Authorization: Bearer <token>`
- Errors return JSON: `{ "message": "..." }`
- Fields and filters will be refined as backend TODOs are completed
