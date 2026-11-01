# 🎂 SweetDelight - Cake Shop Management System

An online food delivery and cake shop web application built using **Django 6**, **Bootstrap 5**, and **SQLite**. The system includes Role-Based Access Control (Admin, Staff, Customer), search and filter capabilities, pagination, event cake pre-booking, shopping cart, wishlist, and payment integration.

---

## 🌟 Key Features

### 1. 👥 Role-Based Access Control (RBAC)
- **Customer**: Browse catalogue, search, filter, add to cart, save to wishlist, pre-book cakes for celebrations, place orders, write reviews, and track order history.
- **Staff / Admin**: Dedicated management dashboard displaying live business metrics (total cakes, pending orders, user counts, and order streams) with access to the Django administration panel.

### 2. 🎂 25 Handcrafted Cakes Catalogue
- 25 popular cakes (Chocolate Truffle, Black Forest, Red Velvet, Lotus Biscoff, Cheesecakes, etc.).
- Categorized under:
  - *Chocolate Delights*
  - *Classic & Cream*
  - *Fresh Fruit Gateaux*
  - *Cheesecakes & Exotic*
- Full product detail view with interactive image galleries, pricing, weights, serving portions, and customer reviews.

### 3. 🔍 Search, Filtering & Pagination
- **Search**: Search cakes by title, flavors, ingredients, and description.
- **Filtering**: By category, price range (Min/Max ₹), and availability status (In-Stock / Pre-Order).
- **Sorting**: Newest, price (low-to-high, high-to-low), and alphabetical.
- **Pagination**: 9 cakes per page.

### 4. 🛒 Cart & Wishlist
- Add to cart with personalized message inscriptions and flavor preferences.
- Dynamic quantity adjustment with subtotal calculations.
- Free shipping threshold indicator (Free delivery above ₹500).
- One-click heart toggle for saving and removing cakes in the wishlist.

### 5. 📅 Event Cake Pre-Booking
- Dedicated scheduling form allowing customers to pre-book custom cakes for birthdays, weddings, and anniversaries.
- Set delivery date, preferred delivery time slot, custom greeting, and specific preparation instructions.

### 6. 💳 Payment Integration
- **Razorpay Payment Gateway**: Supports Cards, UPI (Google Pay, PhonePe), and Netbanking.
- **Cash on Delivery (COD)**: Supports cash payment or QR scan upon delivery.
- Invoice generation and order status updates (`Pending`, `Confirmed`, `Delivered`, `Cancelled`).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Django 6.1
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, Font Awesome 6, Google Fonts
- **Forms**: `django-crispy-forms` with `crispy-bootstrap5`
- **Database**: SQLite3 (default, configurable for PostgreSQL/MySQL)
- **Media & Images**: Pillow (Python Imaging Library)
- **Environment**: `python-decouple`

---

## 📂 Project Architecture

```
Resturant_Application/
├── accounts/               # User authentication, profiles, role management & dashboard
├── cakes/                  # Cake catalogue, categories, search, filtering, and reviews
├── cart/                   # Session & DB Cart, Wishlist, and Context Processors
├── orders/                 # Order checkout, order items, and celebration cake pre-bookings
├── payments/               # Razorpay payment integration & Cash on Delivery (COD)
├── cakeshop/               # Core Django project settings, routes & WSGI configuration
├── templates/              # Master layout and feature-specific HTML templates
├── static/                 # Static assets (custom styles, scripts, icons)
├── media/                  # Uploaded cake thumbnails and gallery images
├── manage.py               # Django management script
├── requirements.txt        # Python package dependencies
├── .env.example            # Sample environment configurations
└── .gitignore              # Ignored files and directories
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ installed
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/neethusanto/cake-shop-management.git
cd cake-shop-management
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Create a `.env` file in the root folder (or use `.env.example`):
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 👤 Default Demo Credentials

| Role | Username | Password |
|---|---|---|
| **Admin / Store Manager** | `admin` | `admin123` |
| **Customer** | `customer` | `customer123` |

*(You can also create a new superuser using `python manage.py createsuperuser`)*

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
