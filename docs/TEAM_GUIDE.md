# Farmart Team Development Guide

**Team Members:**
- **Vanessa** (Team Lead) - Feature 1: Authentication 🧪
- **Tecla** - Feature 2: Animals Listings 🔨
- **Raniel** - Feature 3: Shopping Cart 🔨
- **Jonah** - Feature 4: Orders & Payment 🔨
- **Linda** - Feature 5: QA & Testing 🔨

---

## 🚀 Getting Started (First Time Setup)

### 1. Clone Both Repositories

```bash
# Navigate to your projects folder
cd ~/Development/code/se-prep/phase-5

# Clone backend
git clone https://github.com/Vanessa-Faith/farmart-backend.git
cd farmart-backend

# Clone frontend (go back first)
cd ..
git clone https://github.com/Vanessa-Faith/farmart-frontend.git
cd farmart-frontend
```

### 2. Backend Setup

```bash
cd ~/Development/code/se-prep/phase-5/farmart-backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables (IMPORTANT - READ CAREFULLY!)
cp .env.example .env

# The .env file is already configured with default development settings!
# For local development, you DON'T need to change anything.
# The defaults match the Docker database command below.
#
# OPTIONAL: For extra security, generate new secret keys:
# python -c "import secrets; print(secrets.token_hex(32))"
# Then paste the output into .env for SECRET_KEY and JWT_SECRET_KEY
#
# What's in .env:
# - DATABASE_URL=postgresql://dev:pass@localhost:5432/farmart
#   (matches the Docker container username, password, and database name)
# - SECRET_KEY=dev-secret-key-change-in-production-using-command-above
# - JWT_SECRET_KEY=dev-jwt-secret-change-in-production-using-command-above
# - CORS_ORIGINS=http://localhost:5173 (your frontend URL)
```

**Start PostgreSQL Database:**

The DATABASE_URL in .env connects to this Docker container:

```bash
# This command creates a PostgreSQL database with these settings:
# - Username: dev
# - Password: pass  
# - Database name: farmart
# - Port: 5432
# These match the DATABASE_URL in your .env file!

docker run --name farmart-db \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_USER=dev \
  -e POSTGRES_DB=farmart \
  -p 5432:5432 \
  -d postgres:15

# Check it's running:
docker ps
# You should see 'farmart-db' in the list
```

**Run Database Migrations:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Start Backend Server:**
```bash
python run.py
# Backend runs at http://localhost:5000
```

### 3. Frontend Setup

```bash
cd ~/Development/code/se-prep/phase-5/farmart-frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Make sure VITE_API_URL=http://localhost:5000/api

# Start frontend dev server
npm run dev
# Frontend runs at http://localhost:5173
```

---

## 🌿 Understanding Branches

### Main Branch (`main`)
- **Production code** - what gets deployed
- **Never commit directly to main**
- Only Vanessa (team lead) merges to main after final review
- Think of this as the "official release"

### Dev Branch (`dev`)
- **Integration branch** - where all features come together
- All feature branches merge here first
- This is where we test that features work together
- **Never commit directly to dev**
- Features merge to dev via Pull Requests

### Feature Branches (your work)
- Where YOU write code
- One branch per feature
- Named like: `feature/animals`, `feature/cart`, `feature/orders`, `feature/qa`
- You can commit as much as you want here
- When done, create a Pull Request to merge into `dev`

**Visual:**
```
main (production)
 └── dev (integration)
      ├── feature/animals (Tecla)
      ├── feature/cart (Raniel)
      ├── feature/orders (Jonah)
      └── feature/qa (Linda)
```

---

## 🔨 Daily Workflow (Step-by-Step)

### Step 1: Create Your Feature Branch (FIRST DAY ONLY)

```bash
# Make sure you're in the repo folder
cd ~/Development/code/se-prep/phase-5/farmart-backend  # or farmart-frontend

# Make sure you have latest code
git checkout dev
git pull origin dev

# Create YOUR feature branch (replace with your feature name)
git checkout -b feature/animals     # Tecla
git checkout -b feature/cart        # Raniel
git checkout -b feature/orders      # Jonah
git checkout -b feature/qa          # Linda
git checkout -b feature/auth        # Vanessa (already in testing)

# Push your branch to GitHub (so everyone can see it)
git push -u origin feature/YOUR-FEATURE-NAME
```

### Step 2: Daily Work Routine

**Every morning before you start coding:**
```bash
# Make sure you're on YOUR feature branch
git branch  # Shows which branch you're on (should have * next to yours)

# Get latest changes from dev (in case team made updates)
git checkout dev
git pull origin dev
git checkout feature/YOUR-FEATURE-NAME
git merge dev  # Brings dev changes into your branch
```

**While coding (commit often!):**
```bash
# Check what files you changed
git status

# Stage files you want to commit
git add app/routes/animals.py              # Add specific file
git add src/features/animals/              # Add whole folder
git add .                                  # Add all changed files

# Commit with a descriptive message
git commit -m "Add get all animals endpoint"
git commit -m "Create AnimalList component with filters"
git commit -m "Fix bug in cart quantity update"

# Push to GitHub (backup your work!)
git push origin feature/YOUR-FEATURE-NAME
```

**Good commit messages:** //examples of good commit messages//
- ✅ "Add user registration endpoint with validation"
- ✅ "Create Login form component with error handling"
- ✅ "Fix cart total calculation bug"
- ❌ "updates" (too vague)
- ❌ "fix" (what did you fix?)
- ❌ "asdfasdf" (not helpful)

### Step 3: When Your Feature is Complete

**Before creating Pull Request, test everything:**

1. **Backend testing:**
```bash
# Make sure backend starts without errors
cd ~/Development/code/se-prep/phase-5/farmart-backend
source .venv/bin/activate
python run.py

# Test your endpoints with curl or Postman
curl http://localhost:5000/api/animals
```

2. **Frontend testing:**
```bash
# Make sure frontend builds without errors
cd ~/Development/code/se-prep/phase-5/farmart-frontend
npm run build

# Start dev server and test in browser
npm run dev
# Test your pages, click all buttons, try to break it!
```

3. **End-to-end testing:**
- Start both backend AND frontend
- Test the complete user flow for your feature
- Example for Animals: Browse list → Click animal → See details → Add to cart

**Commit and push final changes:**
```bash
git add .
git commit -m "Complete animals feature - all endpoints and UI working"
git push origin feature/YOUR-FEATURE-NAME
```

---

## 📤 Creating a Pull Request (PR)

### Step 1: Go to GitHub
1. Open browser → https://github.com/Vanessa-Faith/farmart-backend (or frontend)
2. You'll see a yellow banner: "feature/YOUR-FEATURE-NAME had recent pushes"
3. Click **"Compare & pull request"**

### Step 2: Fill Out PR Details

**Title:** Clear and descriptive (example)
```
✅ Feature: Animals Listings (Backend + Frontend)
✅ Feature: Shopping Cart Implementation
❌ Updates (too vague)
```

**Description:** Explain what you built
```markdown
## What I Built (example)
- Backend: CRUD endpoints for animals with search/filter
- Frontend: Animal list page, detail page, create form (farmers)

## Testing Done
- ✅ Tested all endpoints with Postman
- ✅ Tested UI in browser - list, detail, create all work
- ✅ Tested filters (species, price range)
- ✅ Tested farmer-only create form (requires auth)

## Screenshots
[Add screenshots of your UI if frontend work]

## Notes for Reviewer (example)
- Used the auth pattern from Vanessa's auth feature
- Cart integration ready (add-to-cart button in place)
```

**Base branch:** `dev` ← `feature/YOUR-FEATURE-NAME`

### Step 3: Tag Team for Review
- Add **Vanessa** as reviewer (required)
- Add at least 1 other team member as reviewer
- Post in team chat: "PR ready for review: [link]" send link to group chat

---

## 👀 Reviewing Someone's Pull Request

**Your responsibility: Review within 24 hours**

### How to Review: this will be done by Vanessa and one other member

1. **Read the description** - Understand what they built
2. **Check the files changed tab** - Look at their code
3. **Pull their branch locally to test:**

```bash
# Get their branch
git fetch origin
git checkout feature/their-feature-name

# For backend: Start server and test
cd farmart-backend
source .venv/bin/activate
python run.py

# For frontend: Install any new packages and test
cd farmart-frontend
npm install
npm run dev
```

4. **Leave feedback:**
   - ✅ **Approve** if everything works and code looks good
   - 💬 **Comment** if you have questions or suggestions
   - 🔴 **Request changes** if something is broken or needs fixing

**Good review comments:**(xamples)
- "Great work! Tested locally and everything works 🎉"
- "Small suggestion: Could we add error handling on line 45?"
- "This endpoint returns 500 when I test with empty string - can you add validation?"

---

## 🎯 Feature Assignments & Checklist

### Feature 1: Authentication - Vanessa ✅
**Status:** In Testing

**Backend (farmart-backend):**
- ✅ POST /api/auth/register - Create new user with validation
- ✅ POST /api/auth/login - Login and return JWT token
- ✅ GET /api/auth/me - Get current user info

**Frontend (farmart-frontend):**
- ✅ Redux authSlice with loginUser, registerUser, logout
- ✅ Login.jsx - Login form
- ✅ Register.jsx - Registration form
- ✅ PrivateRoute.jsx - Protected route wrapper
- ✅ JWT auto-attached to all API requests

**Next Steps:**
- Test end-to-end
- Create PR when tested

---

### Feature 2: Animals Listings - Tecla 🔨
**Status:** Not Started

**Backend (farmart-backend):**
File: `app/routes/animals.py` (skeleton exists, implement the TODOs)

- [ ] GET /api/animals - List all animals
  - Add search by name/species
  - Add filters (species, min_price, max_price)
  - Add pagination (optional)
  
- [ ] GET /api/animals/:id - Get single animal details

- [ ] POST /api/animals - Create new animal (farmers only)
  - Validate: name, species, price required
  - Check user is authenticated and is a farmer
  
- [ ] PUT /api/animals/:id - Update animal (owner only)
  - Check current user owns this animal
  
- [ ] DELETE /api/animals/:id - Delete animal (owner only)

**Frontend (farmart-frontend):** check in the folder structure to confirm if the files needed are already there
Files to create in `src/features/animals/`

- [ ] `animalsSlice.js` - Redux slice (skeleton exists, complete it)
  - fetchAnimals async thunk
  - fetchAnimalById async thunk
  - createAnimal async thunk (farmers)
  - updateAnimal async thunk (farmers)
  - deleteAnimal async thunk (farmers)

- [ ] `AnimalList.jsx` - Browse animals page
  - Show all animals in cards/grid
  - Search bar
  - Filters (dropdown for species, price range slider)
  - "Add to Cart" button on each card
  
- [ ] `AnimalDetail.jsx` - Single animal page
  - Show all animal details
  - Larger "Add to Cart" button
  - Show farmer info
  
- [ ] `AnimalForm.jsx` - Create/Edit animal (farmers only)
  - Form fields: name, species, description, price, quantity, image_url
  - Validate all fields
  - Submit to backend
  - Redirect to list after success

**Files to update:**
- `src/App.jsx` - Add routes for /animals, /animals/:id, /animals/new, /animals/:id/edit

**Testing Checklist:** more like your objectives
- [ ] Can view list of animals
- [ ] Can search animals by name
- [ ] Can filter by species and price
- [ ] Can click animal to see details
- [ ] Farmers can create new animals
- [ ] Farmers can edit their own animals
- [ ] Farmers can delete their own animals
- [ ] Non-farmers can't access create/edit forms

---

### Feature 3: Shopping Cart - Raniel 🔨
**Status:** Not Started

**Backend (farmart-backend):**
File: `app/routes/carts.py` (skeleton exists, implement the TODOs)

- [ ] GET /api/carts - Get current user's cart with items

- [ ] POST /api/carts/items - Add item to cart
  - Input: animal_id, quantity
  - Validate animal exists and has enough quantity
  - Create cart if user doesn't have one
  - Add to existing cart or update quantity if already in cart
  
- [ ] PUT /api/carts/items/:id - Update cart item quantity
  - Validate new quantity available
  
- [ ] DELETE /api/carts/items/:id - Remove item from cart

**Frontend (farmart-frontend):**check in the folder structure to confirm if the files needed are already there
Files to create in `src/features/cart/`

- [ ] `cartSlice.js` - Redux slice
  - fetchCart async thunk
  - addToCart async thunk
  - updateCartItem async thunk
  - removeFromCart async thunk
  - clearCart action (for after checkout)

- [ ] `Cart.jsx` - Shopping cart page
  - Show all cart items with images, names, prices
  - Quantity controls (+/- buttons) for each item
  - Remove button for each item
  - Show subtotal for each item
  - Show cart total
  - "Checkout" button → navigates to /checkout
  - Empty cart message if no items
  
- [ ] `AddToCartButton.jsx` - Reusable component
  - Props: animalId, currentQuantity
  - Shows "Add to Cart" button
  - Dispatches addToCart action
  - Shows success message/animation
  - Used on AnimalList and AnimalDetail pages

**Files to update:**
- `src/App.jsx` - Add route for /cart
- `src/features/animals/AnimalList.jsx` - Import and use AddToCartButton
- `src/features/animals/AnimalDetail.jsx` - Import and use AddToCartButton

**Testing Checklist:** more like objectives
- [ ] Can add animal to cart from list page
- [ ] Can add animal to cart from detail page
- [ ] Can view cart with all items
- [ ] Can increase item quantity
- [ ] Can decrease item quantity
- [ ] Can remove item from cart
- [ ] Cart total calculates correctly
- [ ] Can't add more than available quantity
- [ ] Cart persists (stored in database)

---

### Feature 4: Orders & Payment - Jonah 🔨
**Status:** Not Started

**Backend (farmart-backend):**
File: `app/routes/orders.py` (skeleton exists, implement the TODOs)

- [ ] GET /api/orders - Get user's orders
  - Buyers see their orders
  - Farmers see orders for their animals
  
- [ ] GET /api/orders/:id - Get single order with all items

- [ ] POST /api/orders - Create order from current cart
  - Validate cart not empty
  - Check all animals still available
  - Create order with pending status
  - Create order_items from cart_items
  - Clear cart after order created
  
- [ ] POST /api/orders/:id/confirm - Farmer confirms order
  - Check current user is the farmer for animals in order
  - Update order status to confirmed
  - Reduce animal quantities
  
- [ ] POST /api/orders/:id/reject - Farmer rejects order
  - Check current user is the farmer
  - Update order status to rejected
  
- [ ] POST /api/orders/:id/pay - Process payment
  - Create payment record (use mock payment for now)
  - Update order status to paid

**Frontend (farmart-frontend):**
Files to create in `src/features/orders/` check in the folder structure to confirm if the files needed are already there

- [ ] `ordersSlice.js` - Redux slice
  - fetchOrders async thunk
  - fetchOrderById async thunk
  - createOrder async thunk
  - confirmOrder async thunk (farmers)
  - rejectOrder async thunk (farmers)
  - payOrder async thunk

- [ ] `Checkout.jsx` - Checkout page
  - Show order summary (items from cart)
  - Show total
  - Payment form (mock - just name and submit)
  - Submit button → creates order + processes payment
  - Redirect to /orders on success
  
- [ ] `OrderHistory.jsx` - Buyer's order history
  - Show all user's orders
  - Show status (pending, confirmed, rejected, paid)
  - Click to see order details
  
- [ ] `OrderDetail.jsx` - Single order view
  - Show all order items
  - Show farmer info
  - Show status
  - Show payment info if paid
  
- [ ] `FarmerOrders.jsx` - Farmer order management (farmers only)
  - Show all orders for farmer's animals
  - Confirm button (changes status to confirmed)
  - Reject button (changes status to rejected)
  - Filter by status

**Files to update:**
- `src/App.jsx` - Add routes for /checkout, /orders, /orders/:id, /farmer/orders
- `src/features/cart/Cart.jsx` - Add checkout button that navigates to /checkout

**Testing Checklist:** more like objectives
- [ ] Can create order from cart
- [ ] Can view order history
- [ ] Can see order details
- [ ] Farmers can see orders for their animals
- [ ] Farmers can confirm orders
- [ ] Farmers can reject orders
- [ ] Can process payment (mock)
- [ ] Order status updates correctly
- [ ] Animal quantities decrease after confirmation

---

### Feature 5: QA & Testing - Linda 🔨
**Status:** Not Started

**Responsibilities:**

1. **Manual Testing (ongoing)**
   - [ ] Test all features as team members complete them
   - [ ] Try to break things (edge cases, invalid inputs)
   - [ ] Test on different browsers (Chrome, Firefox)
   - [ ] Create test data (users, animals, orders)
   - [ ] Document bugs in GitHub Issues

2. **Create Test Data Script**
   File: `db/seed.py` in backend
   - [ ] Create script to populate database with sample data
   - [ ] 5-10 farmers
   - [ ] 5-10 buyers
   - [ ] 20-30 animals (different species, prices)
   - [ ] Some test carts
   - [ ] Some test orders

3. **Write Cypress E2E Tests** (frontend)
   Files in `farmart-frontend/cypress/e2e/`
   
   - [ ] `auth.cy.js` - Test authentication
     - Register new user
     - Login
     - Logout
     - Access protected routes
   
   - [ ] `animals.cy.js` - Test animals feature
     - Browse animals
     - Search/filter
     - View animal details
     - Farmer creates animal
     - Farmer edits animal
   
   - [ ] `cart.cy.js` - Test shopping cart
     - Add to cart
     - Update quantity
     - Remove from cart
     - Cart total calculation
   
   - [ ] `orders.cy.js` - Test orders
     - Checkout flow
     - View order history
     - Farmer confirm/reject order

4. **Setup Cypress** (first time)
```bash
cd farmart-frontend
npm install -D cypress
npx cypress open  # Opens Cypress
```

5. **Bug Reporting Template** (create GitHub issues)
```markdown
**Title:** [Feature] Brief description

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. See error

**Expected Behavior:**
Should show...

**Actual Behavior:**
Shows error...

**Screenshots:**
[Add screenshot]

**Browser:** Chrome 120
```

**Testing Checklist:**  linda's objectives
- [ ] All auth flows work
- [ ] All animals CRUD operations work
- [ ] Cart functionality works
- [ ] Checkout and orders work
- [ ] Farmer order management works
- [ ] Error messages show properly
- [ ] Cypress tests pass
- [ ] Test data seed script works

---

## 🆘 Common Issues & Solutions only if need arises

### "I'm on the wrong branch!"
```bash
# Check which branch you're on
git branch

# Switch to correct branch (don't lose your work!)
git stash  # Saves your changes temporarily
git checkout feature/YOUR-FEATURE
git stash pop  # Brings back your changes
```

### "My branch is behind dev"
```bash
git checkout dev
git pull origin dev
git checkout feature/YOUR-FEATURE
git merge dev
# Fix any conflicts, then:
git add .
git commit -m "Merge dev into feature branch"
git push origin feature/YOUR-FEATURE
```

### "I have merge conflicts"

**What happened:** You and someone else changed the same lines of code. Git doesn't know which version to keep.

**Example:** You added a field to Animal model. Someone else also added a different field to the same model and merged to dev first. When you try to merge dev, Git says "CONFLICT!"

**How to fix:**

1. **Git will mark conflicts in your file with special markers**

When you open the file, you'll see something like this:

```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
<<<<<<< HEAD
    age = db.Column(db.Integer)  # YOUR code (what you added)
=======
    weight = db.Column(db.Float)  # THEIR code (what's in dev)
>>>>>>> dev
    price = db.Column(db.Float)
```

**The markers mean:**
- `<<<<<<< HEAD` - Start of YOUR changes
- `=======` - Divider  
- `>>>>>>> dev` - End of THEIR changes (from dev branch)

2. **Decide what to keep**

**Usually keep BOTH** (most common):
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)  # Keep yours
    weight = db.Column(db.Float)  # Keep theirs too
    price = db.Column(db.Float)
```

**Sometimes keep only YOURS:**
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)  # Only yours
    price = db.Column(db.Float)
```

**Sometimes keep only THEIRS:**
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weight = db.Column(db.Float)  # Only theirs
    price = db.Column(db.Float)
```

3. **Remove the conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)
4. **Save the file**
5. **Tell Git you fixed it:**
```bash
git add filename
git commit -m "Resolve merge conflicts"
git push origin feature/YOUR-FEATURE-NAME
```

**Confused which to keep?** Ask in team chat or ask Vanessa!

### "I committed to dev by accident!"
**IMPORTANT: NEVER commit directly to dev - always use your feature branch!**

1. **STOP!** Don't push if you haven't already
2. **Tell Vanessa immediately** - Post in team chat or DM
3. **Don't try to fix it yourself** - Vanessa will revert the commit
4. **Learn from it:**
   - Always check which branch you're on: `git branch`
   - Before committing, verify: `git branch` should show `* feature/YOUR-FEATURE`
   - If on dev by mistake: `git checkout feature/YOUR-FEATURE` before coding

### "Backend won't start - database error"
```bash
# Make sure PostgreSQL is running
docker ps  # Should see farmart-db container

# If not running, start it
docker start farmart-db

# Re-run migrations
flask db upgrade
```

### "Frontend won't build - module not found"
```bash
# Someone added a new package, reinstall
npm install

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "How do I undo my last commit?"
```bash
# If you haven't pushed yet
git reset --soft HEAD~1  # Keeps your changes, removes commit

# If you already pushed
git revert HEAD  # Creates new commit that undoes the last one
git push
```

---

## 📋 Daily Standup Format (15 minutes)

**Every day at [TIME - Vanessa sets this]**

Each person answers 3 questions:

1. **What did I complete yesterday?**
   - "Finished the GET /animals endpoint with filters"
   - "Created the AnimalList component UI"

2. **What am I working on today?**
   - "Working on POST /animals endpoint"
   - "Adding search functionality to AnimalList"

3. **Any blockers?**
   - "Need help understanding how auth works"
   - "Waiting for Animals feature to test cart"
   - "No blockers!" ✅

**Keep it brief** - detailed discussions happen after standup

---

## ✅ Definition of "Done"

Your feature is done when:

- [x] **Code written** - All endpoints/components implemented
- [x] **Tested locally** - Both backend and frontend work
- [x] **No errors** - Backend starts, frontend builds
- [x] **Code committed** - All changes pushed to your branch
- [x] **PR created** - Pull request submitted
- [x] **Reviewed** - At least 2 approvals (including Vanessa)
- [x] **Merged to dev** - Vanessa merged your PR
- [x] **Works with other features** - Tested integration

---

## 🎓 Learning Resources

### Git & GitHub
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### Backend (Flask)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

### Frontend (React + Redux)
- [React Docs](https://react.dev/)
- [Redux Toolkit Tutorial](https://redux-toolkit.js.org/tutorials/quick-start)

### Testing
- [Cypress Documentation](https://docs.cypress.io/)

---

## 🚨 Emergency Contacts

**Blocked or confused?** Ask for help!

1. **Team Chat** - Post in group chat
2. **Vanessa (Team Lead)** - DM for urgent issues
3. **Team Member** - Pair program with teammate

**Remember:** Asking for help is NOT a weakness. We're a team! 🤝

---

## 🎯 Sprint Timeline

- **Days 1-3** (Jan 29-31): Auth testing + Animals feature
- **Days 4-7** (Feb 1-4): Animals complete + Cart feature
- **Days 8-11** (Feb 5-8): Orders feature + QA testing
- **Days 12-13** (Feb 9-10): Bug fixes + polish
- **Day 14** (Feb 11): Demo rehearsal + final deployment

---

**Good luck team! Let's build something amazing! 🚀**

*Questions? Check this guide first, then ask in team chat!*
