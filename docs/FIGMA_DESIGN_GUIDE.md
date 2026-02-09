# Farmart Figma Design Guide

**Your Goal:** Create simple, clear wireframes that show your team what to build.

**Remember:** Wireframes don't need to be perfect! They're blueprints, not final designs. Focus on layout and functionality.

---

## 🎨 Color Scheme (Farm-Friendly & Professional)

### Primary Colors
```
Primary Green: #10B981 (emerald-500) - Main actions, buttons, links
Dark Green: #047857 (emerald-700) - Headers, emphasis
Light Green: #D1FAE5 (emerald-100) - Backgrounds, highlights
```

### Neutral Colors
```
Dark Gray: #1F2937 (gray-800) - Main text
Medium Gray: #6B7280 (gray-500) - Secondary text
Light Gray: #F3F4F6 (gray-100) - Backgrounds, borders
White: #FFFFFF - Cards, main background
```

### Accent Colors
```
Orange: #F59E0B (amber-500) - Warnings, pending status
Red: #EF4444 (red-500) - Errors, delete actions
Blue: #3B82F6 (blue-500) - Info, links
```

### Status Colors
```
Success: #10B981 (green) - Confirmed orders
Warning: #F59E0B (orange) - Pending orders
Error: #EF4444 (red) - Rejected orders
Info: #3B82F6 (blue) - General info
```

**Pro Tip:** Use these in Figma by creating color styles (click fill → click + icon → save as style)

---

## 📱 Pages You Need to Design (12 Total)

### 1. Authentication Pages (2 pages)

#### Page 1: Register/Signup
**URL:** `/register`

**Elements:**
- [ ] Logo/App name at top
- [ ] "Create Account" heading
- [ ] Form fields:
  - Name (text input)
  - Email (email input)
  - Password (password input)
  - Role dropdown (Farmer / Buyer)
- [ ] "Register" button (green)
- [ ] "Already have account? Login" link

**Layout:** Center card on screen, 400px wide

---

#### Page 2: Login
**URL:** `/login`

**Elements:**
- [ ] Logo/App name at top
- [ ] "Welcome Back" heading
- [ ] Form fields:
  - Email (email input)
  - Password (password input)
- [ ] "Login" button (green)
- [ ] "Don't have account? Register" link

**Layout:** Center card on screen, 400px wide

---

### 2. Animals Pages (4 pages)

#### Page 3: Animals List (Browse)
**URL:** `/animals`

**Elements:**
- [ ] Navigation bar at top (logo, links, cart icon, user dropdown)
- [ ] Page title: "Available Animals"
- [ ] Search bar (with magnifying glass icon)
- [ ] Filters sidebar (left or top):
  - Species dropdown (Cattle, Goats, Sheep, Chickens, Pigs)
  - Price range slider (min-max)
  - "Apply Filters" button
- [ ] Animal cards grid (3-4 per row):
  - Animal image placeholder
  - Name
  - Species
  - Price (large, bold)
  - "View Details" button
  - "Add to Cart" button (for buyers)
- [ ] Pagination (if many animals)

**Layout:** Full width, grid of cards

---

#### Page 4: Animal Detail
**URL:** `/animals/:id`

**Elements:**
- [ ] Navigation bar
- [ ] Back button "← Back to Animals"
- [ ] Large image (left side)
- [ ] Details (right side):
  - Animal name (big heading)
  - Species badge
  - Price (very large)
  - Description
  - Quantity available
  - Farmer info (name, rating if applicable)
- [ ] Quantity selector (+ / - buttons, number input)
- [ ] "Add to Cart" button (large, green) - BUYERS ONLY
- [ ] "Contact Farmer" button (optional)
- [ ] For FARMERS viewing their own:
  - "Edit" button
  - "Delete" button (red)

**Layout:** Two columns - image left, details right

---

#### Page 5: Create Animal (Farmers Only)
**URL:** `/animals/new`

**Elements:**
- [ ] Navigation bar
- [ ] "List New Animal" heading
- [ ] Form in card:
  - Name (text input)
  - Species (dropdown)
  - Description (textarea)
  - Price (number input with $ prefix)
  - Quantity (number input)
  - Image URL (text input) - optional: file upload icon
- [ ] "Cancel" button (gray)
- [ ] "List Animal" button (green)

**Layout:** Center form, 600px wide

---

#### Page 6: Edit Animal (Farmers Only)
**URL:** `/animals/:id/edit`

**Elements:**
- Same as Create Animal page
- Pre-filled with existing data
- Button says "Update Animal" instead of "List Animal"
- Add "Delete Animal" button (red, bottom)

**Layout:** Same as Create

---

### 3. Shopping Cart Pages (1 page)

#### Page 7: Cart
**URL:** `/cart`

**Elements:**
- [ ] Navigation bar
- [ ] "Shopping Cart" heading
- [ ] Cart items list (or "Cart is empty" message):
  - Small image
  - Animal name
  - Price per unit
  - Quantity controls (- button, number, + button)
  - Subtotal (price × quantity)
  - Remove button (X icon, red)
- [ ] Cart summary (right side or bottom):
  - Subtotal
  - Tax (if applicable)
  - **Total** (large, bold)
  - "Checkout" button (large, green)
  - "Continue Shopping" link

**Layout:** List of items (left 70%), summary card (right 30%)

---

### 4. Orders Pages (3 pages)

#### Page 8: Checkout
**URL:** `/checkout`

**Elements:**
- [ ] Navigation bar
- [ ] "Checkout" heading
- [ ] Order summary (items from cart):
  - List of items with quantities
  - Total
- [ ] Payment section (mock):
  - "Payment Information" heading
  - Cardholder name (text input)
  - "Card Number" (text input, placeholder: 4111 1111 1111 1111)
  - Expiry / CVV (smaller inputs)
  - Note: "Using test payment for demo"
- [ ] "Place Order" button (large, green)
- [ ] "Back to Cart" link

**Layout:** Two columns - order summary left, payment form right

---

#### Page 9: Order History (Buyers)
**URL:** `/orders`

**Elements:**
- [ ] Navigation bar
- [ ] "My Orders" heading
- [ ] Filter tabs:
  - All
  - Pending
  - Confirmed
  - Paid
  - Rejected
- [ ] Order cards list:
  - Order number (#12345)
  - Date
  - Total price
  - Status badge (color-coded: pending=orange, confirmed=green, rejected=red)
  - "View Details" button
- [ ] Empty state: "No orders yet"

**Layout:** List view, stacked cards

---

#### Page 10: Order Detail
**URL:** `/orders/:id`

**Elements:**
- [ ] Navigation bar
- [ ] "Order #12345" heading
- [ ] Status badge (large, top)
- [ ] Order info:
  - Order date
  - Status
  - Total
- [ ] Items in order (table or cards):
  - Animal name
  - Quantity
  - Price
  - Subtotal
- [ ] Farmer information
- [ ] Payment information (if paid)
- [ ] "Back to Orders" button

**Layout:** Single column, sections stacked

---

#### Page 11: Farmer Orders Dashboard (Farmers Only)
**URL:** `/farmer/orders`

**Elements:**
- [ ] Navigation bar
- [ ] "Incoming Orders" heading
- [ ] Filter tabs:
  - Pending (show count badge)
  - Confirmed
  - Rejected
- [ ] Order cards:
  - Order number
  - Buyer name
  - Date
  - Items summary (3 goats, 2 chickens)
  - Total price
  - Status
  - Action buttons (for pending only):
    - "Confirm" button (green)
    - "Reject" button (red)
- [ ] Empty state: "No orders"

**Layout:** Grid or list of order cards

---

### 5. Navigation & Layout

#### Page 12: Main Navigation (All Pages)
**URL:** Component used everywhere

**Elements:**
- [ ] Logo/Brand name (left) - links to home
- [ ] Navigation links:
  - "Animals" (all users)
  - "My Cart" with badge showing item count (buyers)
  - "My Orders" (buyers)
  - "My Orders" (farmers - different page)
  - "List Animal" (farmers only)
- [ ] User dropdown (right):
  - User name with avatar/icon
  - Dropdown menu:
    - Profile (optional)
    - Logout

**Layout:** Horizontal bar, sticky at top

---

## 🎯 Design System Components

Create these reusable components in Figma:

### Buttons
1. **Primary Button** (green background, white text)
   - Normal: #10B981
   - Hover: #047857
   - Disabled: #D1D5DB (gray)

2. **Secondary Button** (white background, green border)
   - Border: #10B981
   - Text: #10B981

3. **Danger Button** (red)
   - Background: #EF4444

### Form Inputs
- Text input (border, padding, focus state with green border)
- Dropdown (with arrow icon)
- Number input (with +/- controls)
- Textarea (multiline)

### Cards
- White background
- Border: 1px solid #E5E7EB (light gray)
- Border-radius: 8px
- Padding: 16-24px
- Shadow: subtle (optional)

### Badges/Tags
- Species badge (blue background, white text)
- Status badges (colored: green=confirmed, orange=pending, red=rejected)

### Icons (Use Heroicons or similar)
- Shopping cart
- User
- Search
- Plus/Minus
- Trash
- Edit
- Check
- X (close)

---

## 📐 Layout Guidelines

### Typography
```
Headings:
- H1 (Page titles): 32px, bold, dark gray
- H2 (Section titles): 24px, semi-bold, dark gray
- H3 (Card titles): 18px, semi-bold, dark gray

Body:
- Regular text: 16px, normal, dark gray
- Small text: 14px, normal, medium gray
- Tiny text (labels): 12px, normal, medium gray
```

### Spacing
- Use consistent spacing: 8px, 16px, 24px, 32px, 48px
- Padding inside cards: 24px
- Margin between sections: 32px
- Gap between cards in grid: 24px

### Breakpoints (Mobile-First)
- Mobile: 375px (iPhone)
- Tablet: 768px
- Desktop: 1200px+

**Focus on Desktop first for this project** - mobile can be simplified

---

## 🚀 How to Create in Figma

### Step 1: Setup Frame
1. Create new file: "Farmart Wireframes"
2. Create frames (Press `F`):
   - Desktop: 1440 x 1024
   - Name each frame by page (e.g., "Login", "Animals List")

### Step 2: Create Color Styles
1. Click any shape
2. Fill → Click `+` icon next to color
3. Create styles for each color above
4. Name them: "Primary/Green", "Text/Dark", etc.

### Step 3: Create Components
1. Design one button
2. Select it → Right-click → Create Component (or Ctrl+Alt+K)
3. Repeat for inputs, cards, navbar

### Step 4: Design Pages
1. Start with Login (simplest)
2. Copy navbar component to all other pages
3. Use rectangles for images (gray fill with text "Image")
4. Use text tool for labels
5. Use shapes for buttons, inputs

### Step 5: Add Annotations (Optional but Helpful)
- Add notes in red text explaining interactions
- "Clicking this navigates to Animal Detail page"
- "This dropdown filters by species"

### Step 6: Share with Team
1. Click "Share" (top right)
2. Set to "Anyone with link can view"
3. Copy link
4. Post in team chat

---

## ✅ Quick Checklist

**Must Have (Essential):**
- [ ] 2 Auth pages (Login, Register)
- [ ] 4 Animal pages (List, Detail, Create, Edit)
- [ ] 1 Cart page
- [ ] 3 Order pages (Checkout, History, Farmer Dashboard)
- [ ] 1 Navigation component
- [ ] Color scheme applied consistently
- [ ] Buttons clearly labeled
- [ ] Forms have all required fields

**Nice to Have (Enhancements):**
- [ ] Hover states for buttons
- [ ] Loading states ("Loading..." text)
- [ ] Empty states ("No items in cart")
- [ ] Error states (red border on invalid input)
- [ ] Success messages (green banner at top)
- [ ] User avatars/profile pictures
- [ ] Star ratings for farmers
- [ ] Image placeholders with actual images

**Don't Worry About:**
- ❌ Pixel-perfect designs
- ❌ Custom illustrations
- ❌ Animations
- ❌ Every possible edge case
- ❌ Making it look like a real product

---

## 💡 Pro Tips

1. **Keep it simple** - Boxes and text are fine!
2. **Use real content** - "Dairy Cow - $500" not "Lorem ipsum"
3. **Show the happy path** - One example of each page working correctly
4. **Use placeholders** - Gray boxes for images with text "Product Image 400x300"
5. **Be consistent** - Same button style everywhere, same spacing
6. **Label everything** - Page names, component names, make it obvious
7. **Ask team for feedback** - Share early, iterate

---

## 📋 Your Action Plan

### Tonight (30-45 minutes):
1. ✅ Create Figma file
2. ✅ Set up color styles
3. ✅ Design Login page (start simple!)
4. ✅ Design Register page (copy Login, modify)

### Tomorrow (1 hour):
5. ✅ Design Animals List page
6. ✅ Design Animal Detail page
7. ✅ Design Cart page

### Day After (1 hour):
8. ✅ Design Checkout page
9. ✅ Design Order History page
10. ✅ Design Farmer Orders page
11. ✅ Create Create/Edit Animal pages

### Final (30 min):
12. ✅ Review all pages
13. ✅ Make sure colors are consistent
14. ✅ Share link with team

---

## 🎨 Sample Prompts (If Using AI Design Tools)

If you want to generate design inspiration or use AI:

**For Login Page:**
```
"Design a modern login form for a farm e-commerce platform. 
Clean, minimal design with green color scheme. Center-aligned 
card with email, password fields, and login button. Logo at top."
```

**For Animals List:**
```
"E-commerce product grid for farm animals. Show cards with 
animal image placeholder, name, species tag, price, and 'Add to Cart' 
button. Green and white color scheme. Include search bar and 
filters on left sidebar."
```

**For Cart:**
```
"Shopping cart page for e-commerce site. List items with thumbnail, 
name, quantity controls, price. Summary panel on right with total 
and checkout button. Green color scheme."
```

---

## 📸 Share with Team

Once done, share in group chat:

```
🎨 FIGMA WIREFRAMES READY!

Hi team! I've created wireframes for all our pages:

[Figma Link]

**What's included:**
✅ Login & Register
✅ Animals List, Detail, Create, Edit
✅ Shopping Cart
✅ Checkout & Orders
✅ Farmer Dashboard

**Color Scheme:**
- Primary: Green (#10B981)
- Text: Dark Gray
- Backgrounds: White & Light Gray

These are wireframes (blueprints), not final designs. 
Use them as reference for building your features!

Questions? Let me know! 🚀
```

---

**Remember:** Your team needs clarity, not perfection. Show them WHAT to build, not how pretty it should be. You've got this! 🌟
