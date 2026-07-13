import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:KmtE8wjf%402004@localhost:3306/nutriindia"

engine = create_engine(DATABASE_URL)

query = """
SELECT
    f.food_code,
    f.food_name,
    f.scientific_name,
    f.food_group,

    n.nutrient_code,
    n.display_name,
    n.unit,

    fn.nutrient_value

FROM food_nutrients fn

JOIN foods f
ON fn.food_id = f.id

JOIN nutrients n
ON fn.nutrient_id = n.id

ORDER BY
    f.food_name,
    n.display_name;
"""

df = pd.read_sql(query, engine)

df.to_csv(
    "clean_ifct_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print("Rows:", len(df))