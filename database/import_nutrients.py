import pandas as pd

from database.database import SessionLocal
from database.models import Nutrient
from database.nutrient_mapping import NUTRIENT_MAPPING

# Read CSV
df = pd.read_csv("data/ifct2017_compositions.csv")

# Metadata columns (not nutrients)
metadata = {
    "code",
    "name",
    "scie",
    "regn"
}

# Get only nutrient columns
nutrient_columns = [
    c for c in df.columns
    if c not in metadata
    and not c.endswith("_e")
]

session = SessionLocal()

# Clear existing nutrients (optional during development)
session.query(Nutrient).delete()
session.commit()

nutrient_objects = []

for col in nutrient_columns:

    # Get display name and unit from mapping
    if col in NUTRIENT_MAPPING:
        display_name, unit = NUTRIENT_MAPPING[col]
    else:
        display_name = col.replace("_", " ").title()
        unit = None

    nutrient_objects.append(
        Nutrient(
            nutrient_code=col,
            nutrient_name=display_name,
            display_name=display_name,
            unit=unit
        )
    )

# Bulk insert
session.bulk_save_objects(nutrient_objects)
session.commit()

print(f"✅ Imported {len(nutrient_objects)} nutrients")