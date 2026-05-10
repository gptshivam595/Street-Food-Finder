from __future__ import annotations

from datetime import time

from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.food_item import FoodItem
from app.models.review import Review
from app.models.vendor import Vendor


def parse_time(value: str) -> time:
    return time.fromisoformat(value)


VENDORS = [
    {
        "name": "Indiranagar Chaat Cart",
        "description": "Crisp, tangy North Indian chaat served near the 12th Main evening crowd.",
        "owner_name": "Ramesh Kumar",
        "phone": "+919880100101",
        "area": "Indiranagar",
        "address": "12th Main Road, HAL 2nd Stage, Indiranagar, Bengaluru",
        "latitude": 12.9719,
        "longitude": 77.6412,
        "opening_time": "16:00:00",
        "closing_time": "23:00:00",
        "hygiene_rating": 4.4,
        "food_items": [
            {"name": "Pani Puri", "category": "Chaat", "price": 40},
            {"name": "Dahi Papdi Chaat", "category": "Chaat", "price": 70},
            {"name": "Aloo Tikki Chaat", "category": "Chaat", "price": 80},
            {"name": "Masala Soda", "category": "Juice", "price": 35},
        ],
        "reviews": [
            {"user_name": "Ananya", "rating": 4.7, "hygiene_rating": 4.5, "comment": "Fast service and the pani puri water is properly chilled."},
            {"user_name": "Karthik", "rating": 4.5, "hygiene_rating": 4.3, "comment": "Reliable post-work snack stop."},
            {"user_name": "Meera", "rating": 4.6, "hygiene_rating": 4.4, "comment": "The dahi papdi is balanced and fresh."},
        ],
    },
    {
        "name": "Koramangala Momo Junction",
        "description": "Steamed and fried momos with spicy chutney near the college lanes.",
        "owner_name": "Pema Dorjee",
        "phone": "+919880100102",
        "area": "Koramangala",
        "address": "5th Block, near Jyoti Nivas College, Koramangala, Bengaluru",
        "latitude": 12.9352,
        "longitude": 77.6245,
        "opening_time": "12:00:00",
        "closing_time": "23:30:00",
        "hygiene_rating": 4.2,
        "food_items": [
            {"name": "Veg Steamed Momos", "category": "Momos", "price": 90},
            {"name": "Chicken Fried Momos", "category": "Momos", "price": 130},
            {"name": "Cheese Corn Momos", "category": "Momos", "price": 120},
            {"name": "Lemon Iced Tea", "category": "Tea/Coffee", "price": 50},
        ],
        "reviews": [
            {"user_name": "Riya", "rating": 4.4, "hygiene_rating": 4.2, "comment": "Soft momos and the chutney has a serious kick."},
            {"user_name": "Aditya", "rating": 4.2, "hygiene_rating": 4.1, "comment": "Good portions for the price."},
            {"user_name": "Nisha", "rating": 4.5, "hygiene_rating": 4.3, "comment": "Cheese corn momos are my favorite here."},
            {"user_name": "Varun", "rating": 4.1, "hygiene_rating": 4.0, "comment": "Gets crowded but moves quickly."},
        ],
    },
    {
        "name": "HSR Benne Dosa Stand",
        "description": "Davangere-style dosas finished with butter on a cast iron tawa.",
        "owner_name": "Shivappa Gowda",
        "phone": "+919880100103",
        "area": "HSR Layout",
        "address": "27th Main Road, Sector 2, HSR Layout, Bengaluru",
        "latitude": 12.9121,
        "longitude": 77.6446,
        "opening_time": "07:00:00",
        "closing_time": "12:00:00",
        "hygiene_rating": 4.5,
        "food_items": [
            {"name": "Benne Masala Dosa", "category": "Dosa", "price": 85},
            {"name": "Plain Dosa", "category": "Dosa", "price": 55},
            {"name": "Idli Vada Combo", "category": "Idli/Vada", "price": 60},
            {"name": "Filter Coffee", "category": "Tea/Coffee", "price": 25},
        ],
        "reviews": [
            {"user_name": "Pranav", "rating": 4.8, "hygiene_rating": 4.6, "comment": "Crisp edges, soft center, and excellent chutney."},
            {"user_name": "Lavanya", "rating": 4.6, "hygiene_rating": 4.5, "comment": "Worth waking up early for."},
            {"user_name": "Sanjay", "rating": 4.4, "hygiene_rating": 4.3, "comment": "Coffee is strong and the dosa is buttery."},
        ],
    },
    {
        "name": "Whitefield Roll Express",
        "description": "Hot kati rolls for tech park lunch breaks and late evening cravings.",
        "owner_name": "Imran Sheikh",
        "phone": "+919880100104",
        "area": "Whitefield",
        "address": "ITPL Main Road, Pattandur Agrahara, Whitefield, Bengaluru",
        "latitude": 12.9872,
        "longitude": 77.7361,
        "opening_time": "11:00:00",
        "closing_time": "22:30:00",
        "hygiene_rating": 4.1,
        "food_items": [
            {"name": "Paneer Tikka Roll", "category": "Rolls", "price": 120},
            {"name": "Egg Chicken Roll", "category": "Rolls", "price": 140},
            {"name": "Aloo Roll", "category": "Rolls", "price": 80},
            {"name": "Cold Coffee", "category": "Tea/Coffee", "price": 70},
        ],
        "reviews": [
            {"user_name": "Neeraj", "rating": 4.2, "hygiene_rating": 4.0, "comment": "Good lunch option when meetings run long."},
            {"user_name": "Isha", "rating": 4.3, "hygiene_rating": 4.1, "comment": "Paneer roll has generous filling."},
            {"user_name": "Deepak", "rating": 4.0, "hygiene_rating": 4.0, "comment": "Consistent and quick."},
        ],
    },
    {
        "name": "Marathahalli Pav Bhaji Corner",
        "description": "Buttery pav bhaji and quick snacks near the bridge.",
        "owner_name": "Mahesh Patel",
        "phone": "+919880100105",
        "area": "Marathahalli",
        "address": "Outer Ring Road, near Marathahalli Bridge, Bengaluru",
        "latitude": 12.9569,
        "longitude": 77.7011,
        "opening_time": "17:00:00",
        "closing_time": "01:00:00",
        "hygiene_rating": 3.9,
        "food_items": [
            {"name": "Butter Pav Bhaji", "category": "Pav Bhaji", "price": 110},
            {"name": "Cheese Pav Bhaji", "category": "Pav Bhaji", "price": 140},
            {"name": "Tawa Pulao", "category": "Snacks", "price": 120},
            {"name": "Fresh Lime Juice", "category": "Juice", "price": 45},
        ],
        "reviews": [
            {"user_name": "Sowmya", "rating": 4.1, "hygiene_rating": 3.9, "comment": "Late-night lifesaver with hot pav."},
            {"user_name": "Rahul", "rating": 4.0, "hygiene_rating": 3.8, "comment": "Bhaji is rich and spicy."},
            {"user_name": "Farah", "rating": 3.9, "hygiene_rating": 3.8, "comment": "Good taste, busy roadside setup."},
            {"user_name": "Manoj", "rating": 4.2, "hygiene_rating": 4.0, "comment": "Cheese pav bhaji is filling."},
        ],
    },
    {
        "name": "MG Road Sandwich Hub",
        "description": "Grilled sandwiches and fresh juice for office-goers near the boulevard.",
        "owner_name": "Joseph Dsouza",
        "phone": "+919880100106",
        "area": "MG Road",
        "address": "Church Street junction, MG Road, Bengaluru",
        "latitude": 12.9758,
        "longitude": 77.6067,
        "opening_time": "10:00:00",
        "closing_time": "21:30:00",
        "hygiene_rating": 4.3,
        "food_items": [
            {"name": "Bombay Grilled Sandwich", "category": "Sandwich", "price": 85},
            {"name": "Cheese Corn Sandwich", "category": "Sandwich", "price": 100},
            {"name": "Watermelon Juice", "category": "Juice", "price": 60},
            {"name": "Chocolate Sandwich", "category": "Desserts", "price": 95},
        ],
        "reviews": [
            {"user_name": "Arjun", "rating": 4.3, "hygiene_rating": 4.4, "comment": "Clean counter and neatly packed sandwiches."},
            {"user_name": "Tanya", "rating": 4.2, "hygiene_rating": 4.2, "comment": "Great quick bite before metro."},
            {"user_name": "Naveen", "rating": 4.1, "hygiene_rating": 4.3, "comment": "Watermelon juice tasted fresh."},
        ],
    },
    {
        "name": "Jayanagar Idli House",
        "description": "Soft idlis, crisp vadas, and coconut chutney from early morning.",
        "owner_name": "Lakshmi Narayan",
        "phone": "+919880100107",
        "area": "Jayanagar",
        "address": "4th Block Market, Jayanagar, Bengaluru",
        "latitude": 12.9250,
        "longitude": 77.5938,
        "opening_time": "06:00:00",
        "closing_time": "11:30:00",
        "hygiene_rating": 4.7,
        "food_items": [
            {"name": "Thatte Idli", "category": "Idli/Vada", "price": 35},
            {"name": "Medu Vada", "category": "Idli/Vada", "price": 30},
            {"name": "Kesari Bath", "category": "Desserts", "price": 40},
            {"name": "Filter Coffee", "category": "Tea/Coffee", "price": 25},
        ],
        "reviews": [
            {"user_name": "Sahana", "rating": 4.9, "hygiene_rating": 4.8, "comment": "Simple breakfast done perfectly."},
            {"user_name": "Vikram", "rating": 4.6, "hygiene_rating": 4.7, "comment": "Very clean and organized."},
            {"user_name": "Pooja", "rating": 4.7, "hygiene_rating": 4.6, "comment": "Chutney is fresh every time."},
        ],
    },
    {
        "name": "BTM Juice and Snacks",
        "description": "Fruit juices, chaats, and small snacks for the BTM student crowd.",
        "owner_name": "Ganesh Rao",
        "phone": "+919880100108",
        "area": "BTM Layout",
        "address": "7th Main Road, BTM Layout Stage 2, Bengaluru",
        "latitude": 12.9166,
        "longitude": 77.6101,
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "hygiene_rating": 4.0,
        "food_items": [
            {"name": "Mosambi Juice", "category": "Juice", "price": 55},
            {"name": "Mango Milkshake", "category": "Juice", "price": 80},
            {"name": "Masala Puri", "category": "Chaat", "price": 60},
            {"name": "Samosa Plate", "category": "Snacks", "price": 45},
        ],
        "reviews": [
            {"user_name": "Harish", "rating": 4.0, "hygiene_rating": 4.0, "comment": "Affordable and refreshing."},
            {"user_name": "Aditi", "rating": 4.1, "hygiene_rating": 4.1, "comment": "Mosambi juice is dependable."},
            {"user_name": "Kunal", "rating": 3.9, "hygiene_rating": 3.8, "comment": "Good evening snack stop."},
        ],
    },
    {
        "name": "Electronic City Tea Kada",
        "description": "Strong tea, bun maska, and office-break snacks beside the service road.",
        "owner_name": "Murugan S",
        "phone": "+919880100109",
        "area": "Electronic City",
        "address": "Phase 1, near Wipro Gate, Electronic City, Bengaluru",
        "latitude": 12.8892,
        "longitude": 77.6602,
        "opening_time": "05:30:00",
        "closing_time": "23:30:00",
        "hygiene_rating": 3.8,
        "food_items": [
            {"name": "Ginger Tea", "category": "Tea/Coffee", "price": 15},
            {"name": "Bun Maska", "category": "Snacks", "price": 35},
            {"name": "Onion Samosa", "category": "Snacks", "price": 20},
            {"name": "Cold Badam Milk", "category": "Desserts", "price": 50},
        ],
        "reviews": [
            {"user_name": "Siddharth", "rating": 4.0, "hygiene_rating": 3.8, "comment": "Tea is strong and open almost all day."},
            {"user_name": "Maya", "rating": 3.8, "hygiene_rating": 3.7, "comment": "Good for a quick office break."},
            {"user_name": "Girish", "rating": 3.9, "hygiene_rating": 3.8, "comment": "Bun maska with ginger tea hits the spot."},
        ],
    },
    {
        "name": "Bellandur Dessert Cart",
        "description": "Kulfi, falooda, and chilled sweets beside the lake traffic stretch.",
        "owner_name": "Sameer Khan",
        "phone": "+919880100110",
        "area": "Bellandur",
        "address": "Sarjapur Road, near Bellandur Central, Bengaluru",
        "latitude": 12.9304,
        "longitude": 77.6784,
        "opening_time": "15:00:00",
        "closing_time": "00:30:00",
        "hygiene_rating": 4.2,
        "food_items": [
            {"name": "Malai Kulfi", "category": "Desserts", "price": 60},
            {"name": "Rose Falooda", "category": "Desserts", "price": 110},
            {"name": "Chocolate Kulfi", "category": "Desserts", "price": 70},
            {"name": "Sweet Lassi", "category": "Juice", "price": 65},
        ],
        "reviews": [
            {"user_name": "Priya", "rating": 4.4, "hygiene_rating": 4.3, "comment": "Falooda is rich and neatly served."},
            {"user_name": "Rohan", "rating": 4.2, "hygiene_rating": 4.1, "comment": "Great after dinner stop."},
            {"user_name": "Divya", "rating": 4.3, "hygiene_rating": 4.2, "comment": "Kulfi texture is excellent."},
        ],
    },
    {
        "name": "Malleswaram Masala Dosa Point",
        "description": "Classic Bengaluru dosa near Sampige Road with coconut chutney.",
        "owner_name": "Narasimha Bhat",
        "phone": "+919880100111",
        "area": "Malleswaram",
        "address": "Sampige Road, Malleswaram, Bengaluru",
        "latitude": 13.0031,
        "longitude": 77.5709,
        "opening_time": "07:00:00",
        "closing_time": "21:00:00",
        "hygiene_rating": 4.6,
        "food_items": [
            {"name": "Masala Dosa", "category": "Dosa", "price": 75},
            {"name": "Rava Dosa", "category": "Dosa", "price": 85},
            {"name": "Vada Sambar", "category": "Idli/Vada", "price": 45},
            {"name": "Badam Milk", "category": "Desserts", "price": 55},
        ],
        "reviews": [
            {"user_name": "Sharath", "rating": 4.7, "hygiene_rating": 4.6, "comment": "Old-school flavor and very clean."},
            {"user_name": "Rachana", "rating": 4.5, "hygiene_rating": 4.5, "comment": "Rava dosa is crisp and light."},
            {"user_name": "Gautham", "rating": 4.6, "hygiene_rating": 4.7, "comment": "Fast service despite the queue."},
        ],
    },
    {
        "name": "Rajajinagar Chilli Bajji Stop",
        "description": "Hot bajjis, bondas, and tea for rainy evenings.",
        "owner_name": "Manjunath H",
        "phone": "+919880100112",
        "area": "Rajajinagar",
        "address": "Dr Rajkumar Road, Rajajinagar, Bengaluru",
        "latitude": 12.9915,
        "longitude": 77.5546,
        "opening_time": "15:30:00",
        "closing_time": "22:30:00",
        "hygiene_rating": 3.7,
        "food_items": [
            {"name": "Mirchi Bajji", "category": "Snacks", "price": 35},
            {"name": "Mangalore Bonda", "category": "Snacks", "price": 40},
            {"name": "Masala Tea", "category": "Tea/Coffee", "price": 20},
            {"name": "Pineapple Kesari", "category": "Desserts", "price": 45},
        ],
        "reviews": [
            {"user_name": "Chethan", "rating": 3.9, "hygiene_rating": 3.7, "comment": "Perfect with tea on cloudy days."},
            {"user_name": "Keerthi", "rating": 4.0, "hygiene_rating": 3.8, "comment": "Bajjis are always hot."},
            {"user_name": "Nikhil", "rating": 3.8, "hygiene_rating": 3.6, "comment": "Simple snacks, quick service."},
        ],
    },
    {
        "name": "Basavanagudi Congress Bun Cart",
        "description": "Spicy peanut buns, coffee, and quick South Bengaluru bites.",
        "owner_name": "Venkatesh Murthy",
        "phone": "+919880100113",
        "area": "Basavanagudi",
        "address": "Gandhi Bazaar Main Road, Basavanagudi, Bengaluru",
        "latitude": 12.9432,
        "longitude": 77.5738,
        "opening_time": "08:00:00",
        "closing_time": "21:00:00",
        "hygiene_rating": 4.1,
        "food_items": [
            {"name": "Congress Bun", "category": "Snacks", "price": 35},
            {"name": "Masala Sandwich", "category": "Sandwich", "price": 70},
            {"name": "Filter Coffee", "category": "Tea/Coffee", "price": 25},
            {"name": "Carrot Halwa Cup", "category": "Desserts", "price": 60},
        ],
        "reviews": [
            {"user_name": "Bhavana", "rating": 4.2, "hygiene_rating": 4.1, "comment": "Congress bun has the right peanut crunch."},
            {"user_name": "Raghav", "rating": 4.1, "hygiene_rating": 4.0, "comment": "Coffee is always fresh."},
            {"user_name": "Sneha", "rating": 4.0, "hygiene_rating": 4.1, "comment": "Good stop during Gandhi Bazaar shopping."},
        ],
    },
    {
        "name": "Frazer Town Shawarma Roll Van",
        "description": "Juicy rolls and quick grilled snacks near Mosque Road.",
        "owner_name": "Aftab Ahmed",
        "phone": "+919880100114",
        "area": "Frazer Town",
        "address": "Mosque Road, Frazer Town, Bengaluru",
        "latitude": 12.9985,
        "longitude": 77.6159,
        "opening_time": "18:00:00",
        "closing_time": "02:00:00",
        "hygiene_rating": 4.0,
        "food_items": [
            {"name": "Chicken Shawarma Roll", "category": "Rolls", "price": 130},
            {"name": "Paneer Shawarma Roll", "category": "Rolls", "price": 110},
            {"name": "Peri Peri Fries", "category": "Snacks", "price": 90},
            {"name": "Mint Lime", "category": "Juice", "price": 45},
        ],
        "reviews": [
            {"user_name": "Zara", "rating": 4.3, "hygiene_rating": 4.0, "comment": "Late-night roll cravings sorted."},
            {"user_name": "Faizan", "rating": 4.2, "hygiene_rating": 3.9, "comment": "Good meat and fresh bread."},
            {"user_name": "Shreya", "rating": 4.0, "hygiene_rating": 4.0, "comment": "Paneer roll is flavorful."},
        ],
    },
    {
        "name": "Banashankari Bhel House",
        "description": "Dry bhel, sev puri, and fruit juice near the bus stand.",
        "owner_name": "Nitin Shah",
        "phone": "+919880100115",
        "area": "Banashankari",
        "address": "2nd Stage, near Banashankari Bus Stand, Bengaluru",
        "latitude": 12.9150,
        "longitude": 77.5736,
        "opening_time": "14:00:00",
        "closing_time": "22:00:00",
        "hygiene_rating": 4.0,
        "food_items": [
            {"name": "Bhel Puri", "category": "Chaat", "price": 55},
            {"name": "Sev Puri", "category": "Chaat", "price": 65},
            {"name": "Veg Cheese Sandwich", "category": "Sandwich", "price": 90},
            {"name": "Sugarcane Juice", "category": "Juice", "price": 35},
        ],
        "reviews": [
            {"user_name": "Akash", "rating": 4.1, "hygiene_rating": 4.0, "comment": "Dry bhel stays crunchy."},
            {"user_name": "Janani", "rating": 4.0, "hygiene_rating": 4.1, "comment": "Fresh toppings and quick service."},
            {"user_name": "Omkar", "rating": 3.9, "hygiene_rating": 3.9, "comment": "Good for an evening snack."},
        ],
    },
    {
        "name": "Yelahanka College Momos",
        "description": "Budget momo plates and hot tea around the student lanes.",
        "owner_name": "Tenzin Norbu",
        "phone": "+919880100116",
        "area": "Yelahanka",
        "address": "New Town Main Road, Yelahanka, Bengaluru",
        "latitude": 13.0644,
        "longitude": 77.5963,
        "opening_time": "13:00:00",
        "closing_time": "22:30:00",
        "hygiene_rating": 3.9,
        "food_items": [
            {"name": "Veg Momos", "category": "Momos", "price": 70},
            {"name": "Schezwan Fried Momos", "category": "Momos", "price": 100},
            {"name": "Honey Chilli Potato", "category": "Snacks", "price": 90},
            {"name": "Lemon Tea", "category": "Tea/Coffee", "price": 25},
        ],
        "reviews": [
            {"user_name": "Mohan", "rating": 4.0, "hygiene_rating": 3.9, "comment": "Good prices for students."},
            {"user_name": "Reema", "rating": 3.9, "hygiene_rating": 3.8, "comment": "Fried momos are crisp."},
            {"user_name": "Irfan", "rating": 4.1, "hygiene_rating": 4.0, "comment": "Chutney is bold and fresh."},
        ],
    },
    {
        "name": "Sarjapur Road Millet Dosa Stall",
        "description": "Millet dosas and healthy breakfast plates for early commuters.",
        "owner_name": "Pushpa R",
        "phone": "+919880100117",
        "area": "Sarjapur Road",
        "address": "Kaikondrahalli, Sarjapur Road, Bengaluru",
        "latitude": 12.9136,
        "longitude": 77.6854,
        "opening_time": "06:30:00",
        "closing_time": "13:00:00",
        "hygiene_rating": 4.5,
        "food_items": [
            {"name": "Ragi Dosa", "category": "Dosa", "price": 75},
            {"name": "Set Dosa", "category": "Dosa", "price": 70},
            {"name": "Idli Plate", "category": "Idli/Vada", "price": 45},
            {"name": "Fresh Orange Juice", "category": "Juice", "price": 70},
        ],
        "reviews": [
            {"user_name": "Charu", "rating": 4.5, "hygiene_rating": 4.6, "comment": "Light breakfast and very neat setup."},
            {"user_name": "Ritesh", "rating": 4.4, "hygiene_rating": 4.5, "comment": "Ragi dosa is surprisingly tasty."},
            {"user_name": "Aparna", "rating": 4.6, "hygiene_rating": 4.5, "comment": "Fresh chutney and quick service."},
        ],
    },
    {
        "name": "Kalyan Nagar Pav and Sandwich",
        "description": "Fusion sandwiches, pav snacks, and cold beverages near HRBR Layout.",
        "owner_name": "Dinesh Mehta",
        "phone": "+919880100118",
        "area": "Kalyan Nagar",
        "address": "HRBR Layout 2nd Block, Kalyan Nagar, Bengaluru",
        "latitude": 13.0246,
        "longitude": 77.6409,
        "opening_time": "11:00:00",
        "closing_time": "23:00:00",
        "hygiene_rating": 4.2,
        "food_items": [
            {"name": "Paneer Pav Bhaji", "category": "Pav Bhaji", "price": 130},
            {"name": "Tandoori Mayo Sandwich", "category": "Sandwich", "price": 110},
            {"name": "Masala Fries", "category": "Snacks", "price": 80},
            {"name": "Cold Coffee", "category": "Tea/Coffee", "price": 75},
        ],
        "reviews": [
            {"user_name": "Joel", "rating": 4.2, "hygiene_rating": 4.1, "comment": "Good variety and clean prep counter."},
            {"user_name": "Mitali", "rating": 4.3, "hygiene_rating": 4.2, "comment": "Sandwich is flavorful and filling."},
            {"user_name": "Kiran", "rating": 4.1, "hygiene_rating": 4.1, "comment": "Pav bhaji has a nice buttery finish."},
        ],
    },
    {
        "name": "JP Nagar Sweet Corn and Juice",
        "description": "Steamed corn cups, seasonal juices, and quick school-time snacks.",
        "owner_name": "Suresh P",
        "phone": "+919880100119",
        "area": "JP Nagar",
        "address": "24th Main Road, JP Nagar 6th Phase, Bengaluru",
        "latitude": 12.9063,
        "longitude": 77.5857,
        "opening_time": "10:30:00",
        "closing_time": "22:00:00",
        "hygiene_rating": 4.3,
        "food_items": [
            {"name": "Masala Sweet Corn", "category": "Snacks", "price": 50},
            {"name": "Cheese Corn Cup", "category": "Snacks", "price": 70},
            {"name": "Pomegranate Juice", "category": "Juice", "price": 90},
            {"name": "Fruit Custard Cup", "category": "Desserts", "price": 65},
        ],
        "reviews": [
            {"user_name": "Namrata", "rating": 4.3, "hygiene_rating": 4.4, "comment": "Corn is fresh and neatly served."},
            {"user_name": "Tejas", "rating": 4.1, "hygiene_rating": 4.2, "comment": "Juices are not too sugary."},
            {"user_name": "Renu", "rating": 4.2, "hygiene_rating": 4.3, "comment": "Good light snack option."},
        ],
    },
    {
        "name": "Domlur Kathi Roll and Chai",
        "description": "Kathi rolls, cutting chai, and small bites for office commuters.",
        "owner_name": "Santosh Gupta",
        "phone": "+919880100120",
        "area": "Domlur",
        "address": "Old Airport Road, Domlur, Bengaluru",
        "latitude": 12.9606,
        "longitude": 77.6387,
        "opening_time": "08:00:00",
        "closing_time": "23:45:00",
        "hygiene_rating": 4.1,
        "food_items": [
            {"name": "Double Egg Roll", "category": "Rolls", "price": 95},
            {"name": "Paneer Bhurji Roll", "category": "Rolls", "price": 125},
            {"name": "Cutting Chai", "category": "Tea/Coffee", "price": 20},
            {"name": "Bread Pakora", "category": "Snacks", "price": 45},
        ],
        "reviews": [
            {"user_name": "Abhinav", "rating": 4.2, "hygiene_rating": 4.1, "comment": "Rolls are hot and wrapped well."},
            {"user_name": "Leena", "rating": 4.0, "hygiene_rating": 4.0, "comment": "Chai is strong and cheap."},
            {"user_name": "Tarun", "rating": 4.1, "hygiene_rating": 4.1, "comment": "Paneer bhurji roll is excellent."},
        ],
    },
]


def seed_vendors(db: Session) -> tuple[int, int, int]:
    print("Seeding vendors...")
    print("Seeding food items...")
    print("Seeding reviews...")
    vendor_count = 0
    food_count = 0
    review_count = 0

    for data in VENDORS:
        existing = db.query(Vendor).filter(Vendor.name == data["name"]).first()
        if existing:
            continue
        reviews = data["reviews"]
        avg_rating = sum(review["rating"] for review in reviews) / len(reviews)
        avg_hygiene = sum(review["hygiene_rating"] for review in reviews) / len(reviews)
        vendor = Vendor(
            name=data["name"],
            description=data["description"],
            owner_name=data["owner_name"],
            phone=data["phone"],
            area=data["area"],
            address=data["address"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            opening_time=parse_time(data["opening_time"]),
            closing_time=parse_time(data["closing_time"]),
            hygiene_rating=round(avg_hygiene, 2),
            average_rating=round(avg_rating, 2),
            review_count=len(reviews),
        )
        db.add(vendor)
        db.flush()
        vendor_count += 1

        for item in data["food_items"]:
            db.add(FoodItem(vendor_id=vendor.id, **item))
            food_count += 1

        for review in reviews:
            db.add(Review(vendor_id=vendor.id, **review))
            review_count += 1

    db.commit()
    return vendor_count, food_count, review_count


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        vendor_count, food_count, review_count = seed_vendors(db)
        print(f"Seeded {vendor_count} vendors")
        print(f"Seeded {food_count} food items")
        print(f"Seeded {review_count} reviews")
        print("Seed complete")
    finally:
        db.close()


if __name__ == "__main__":
    main()
