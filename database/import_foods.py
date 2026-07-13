import pandas as pd

from database.database import SessionLocal
from database.models import Food

# Read CSV
df = pd.read_csv("data/ifct2017_compositions.csv")

session = SessionLocal()

# Remove old data (optional during development)
session.query(Food).delete()
session.commit()

foods = []

for _, row in df.iterrows():

    food = Food(
        food_code=str(row["code"]),
        food_name=str(row["name"]),
        scientific_name=None if pd.isna(row["scie"]) else str(row["scie"]),
        food_group=str(row["regn"])
    )

    foods.append(food)

session.bulk_save_objects(foods)
session.commit()

print(f"✅ Imported {len(foods)} foods")