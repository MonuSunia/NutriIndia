import pandas as pd
from tqdm import tqdm

from database.database import SessionLocal
from database.models import Food, Nutrient, FoodNutrient

# -------------------------
# Load IFCT dataset
# -------------------------

df = pd.read_csv("data/ifct2017_compositions.csv")

metadata = {
    "code",
    "name",
    "scie",
    "regn"
}

nutrient_columns = [
    c for c in df.columns
    if c not in metadata
    and not c.endswith("_e")
]

session = SessionLocal()

# -------------------------
# Build lookup dictionaries
# -------------------------

foods = session.query(Food).all()

food_lookup = {
    f.food_code: f.id
    for f in foods
}

nutrients = session.query(Nutrient).all()

nutrient_lookup = {
    n.nutrient_code: n.id
    for n in nutrients
}

# -------------------------
# Remove previous data
# -------------------------

session.query(FoodNutrient).delete()
session.commit()

batch = []

BATCH_SIZE = 5000

total_inserted = 0

# -------------------------
# Import
# -------------------------

for _, row in tqdm(df.iterrows(), total=len(df)):

    food_code = str(row["code"])

    food_id = food_lookup.get(food_code)

    if food_id is None:
        continue

    for nutrient in nutrient_columns:

        value = row[nutrient]

        if pd.isna(value):
            continue

        nutrient_id = nutrient_lookup.get(nutrient)

        if nutrient_id is None:
            continue

        batch.append(

            FoodNutrient(

                food_id=food_id,

                nutrient_id=nutrient_id,

                nutrient_value=float(value)

            )

        )

        if len(batch) >= BATCH_SIZE:

            session.bulk_save_objects(batch)

            session.commit()

            total_inserted += len(batch)

            print(f"Inserted {total_inserted:,}")

            batch = []

# Insert remaining rows

if batch:

    session.bulk_save_objects(batch)

    session.commit()

    total_inserted += len(batch)

session.close()

print("=" * 50)

print("Import Finished")

print(f"Rows inserted : {total_inserted:,}")