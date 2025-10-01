import os
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "Eco-Track"
COLLECTION_NAME = "departments"

def seed_departments():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Your existing department IDs (replace with the ones you used for devices)
    department_ids = [
        ObjectId("66fb7a1123a9cdddcf01aa11"),
        ObjectId("66fb7a1123a9cdddcf01aa12"),
        ObjectId("66fb7a1123a9cdddcf01aa13"),
        ObjectId("66fb7a1123a9cdddcf01aa14"),
        ObjectId("66fb7a1123a9cdddcf01aa15"),
    ]

    # Define 5 departments
    departments = [
        {
            "_id": department_ids[0],
            "name": "IT Department",
            "employee_count": 20,
            "expected_power_intensity": 1.5,
            "department_type": "IT",
            "admin_id": None,
            "is_active": True,
        },
        {
            "_id": department_ids[1],
            "name": "HR Department",
            "employee_count": 10,
            "expected_power_intensity": 1.1,
            "department_type": "HR",
            "admin_id": None,
            "is_active": True,
        },
        {
            "_id": department_ids[2],
            "name": "Finance Department",
            "employee_count": 15,
            "expected_power_intensity": 1.3,
            "department_type": "Finance",
            "admin_id": None,
            "is_active": True,
        },
        {
            "_id": department_ids[3],
            "name": "Operations Department",
            "employee_count": 25,
            "expected_power_intensity": 1.7,
            "department_type": "Operations",
            "admin_id": None,
            "is_active": True,
        },
        {
            "_id": department_ids[4],
            "name": "Marketing Department",
            "employee_count": 12,
            "expected_power_intensity": 1.2,
            "department_type": "Marketing",
            "admin_id": None,
            "is_active": True,
        },
    ]

    # Optional: clear collection
    collection.delete_many({})

    # Insert departments
    result = collection.insert_many(departments)
    print(f"Inserted {len(result.inserted_ids)} departments into '{COLLECTION_NAME}'")

    client.close()

if __name__ == "__main__":
    seed_departments()
