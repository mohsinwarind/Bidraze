


# Bidraze - Auction Web Application

**Bidraze** is a feature-rich online auction platform built with **Python** and **Django**. It allows users to create listings, place bids, track items via a watchlist, and manage auctions in a user-friendly interface. The application is deployed on **Render** for reliable hosting and performance.

---

## Features

### 1. **User Authentication**
- **Sign Up** – Create a new account to participate in auctions.
- **Login** – Secure user login to access personalized features.
- **Logout** – Safely log out of your account.

### 2. **Auction Listings**
- **Active Listings** – Browse all ongoing auctions.
- **Create Listing** – Registered users can list new items for auction.
- **Categories** – Filter auction items by category for easier navigation.
- **Close Listing** – Listers can close the bidding for their own auctions.

### 3. **Watchlist**
- Users can **add auctions to their personal watchlist** to monitor bidding activity easily.

### 4. **Bidding & Comments**
- **Place Bids** – Users can place bids on active auctions.
- **Add Comments** – Users can comment on any auction listing to interact or ask questions.



## User Roles

### **1. Viewer**
- Browse active listings.
- Add items to watchlist.
- Place bids on open auctions.
- Post comments on auction listings.

### **2. Lister (Seller)**
- Create and manage auction listings.
- Close the auction at any time.

---

## Technology Stack

- **Backend:** Python 3.x, Django Framework.
- **Frontend:** Django templates, HTML5, CSS3, JavaScript.
- **Database:** SQLite3 (default for Django).
- **Deployment:** Render Cloud Platform.

---

## Installation & Setup (Local)

Follow these steps to run the project locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/bidraze.git
cd bidraze
````

### **2. Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**

```bash
python manage.py migrate
```

### **5. Run the Development Server**

```bash
python manage.py runserver
```

Access the app at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## Deployment

The application is deployed on **Render** for production hosting.
[Visit Bidraze Online](https://bidraze.onrender.com)

---

## Project Structure

```
Bidraze/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├──commerce /        # Main project 
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── auctions/       # Core app containing auction logic
    ├── models.py   # Database models (Listings, Bids, Comments)
    ├── views.py    # View logic for pages
    ├── urls.py     # App-specific routes
    ├── templates/  # HTML templates
    └── static/     # CSS, JS, Images
```

---

## Future Enhancements

* **Email notifications** for winning bids.
* **Image uploads** for listings.
* **Payment integration** (Stripe/PayPal).
* **Mobile-responsive UI improvements.**

---

## License

## License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute the code with proper attribution.

See the [LICENSE](LICENSE) file for more details.

---

## Author

Coded with love by **Mohsin Ramzan** (https://mohsin-jade.vercel.app/).

