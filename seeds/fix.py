from pymongo import MongoClient
import os

# 1. Connect to your DB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "Eco-Track"        # same name you used in Atlas
COLLECTION_NAME = "devices"  # collection you want to seed

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
devices = db[COLLECTION_NAME]

# 2. Define realistic ranges
def correct_power_rating(device_type, current_rating):
    try:
        rating = int(str(current_rating).replace("W", "").strip())
    except:
        return None

    if device_type == "desktop":
        if rating < 200:
            return "250W"
        elif rating > 400:
            return "350W"
        else:
            return f"{rating}W"

    elif device_type == "laptop":
        if rating < 40:
            return "60W"
        elif rating > 150:
            return "120W"
        else:
            return f"{rating}W"

    else:
        return f"{rating}W"


# 3. Loop through and update
for device in devices.find():
    device_type = device.get("type", "").lower()
    current_rating = device.get("powerRating")

    corrected = correct_power_rating(device_type, current_rating)

    if corrected and corrected != current_rating:
        devices.update_one(
            {"_id": device["_id"]},
            {"$set": {"powerRating": corrected}}
        )
        print(f"Updated {device['deviceName']} ({device_type}) from {current_rating} -> {corrected}")

print("✅ Power ratings corrected successfully.")
