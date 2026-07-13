import pandas as pd

from database.database import SessionLocal
from database.models import Food, Nutrient, FoodNutrient

FILE = "ifct2017_compositions.csv"

df = pd.read_csv(FILE)

session = SessionLocal()

# Metadata columns in your dataset
metadata = {
    "code",
    "name",
    "scie",
    "regn"
}

# Keep only nutrient columns (exclude *_e quality columns)
nutrient_columns = [
    c for c in df.columns
    if c not in metadata and not c.endswith("_e")
]

print(f"Foods: {len(df)}")
print(f"Nutrients: {len(nutrient_columns)}")