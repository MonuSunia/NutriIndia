from database.database import Base, engine

# Import models so SQLAlchemy knows about them
from database.models import Food, Nutrient, FoodNutrient

Base.metadata.create_all(bind=engine)

print("✅ Database created successfully!")