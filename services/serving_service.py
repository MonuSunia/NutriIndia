import streamlit as st
import pandas as pd

from database.database import SessionLocal
from database.models import Food, Nutrient, FoodNutrient


# ==========================================================
# Get Foods
# ==========================================================

@st.cache_data(show_spinner=False)
def get_foods():

    session = SessionLocal()

    try:

        return (
            session.query(Food)
            .order_by(Food.food_name)
            .all()
        )

    finally:
        session.close()


# ==========================================================
# Get Nutrients of Food
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food_profile(food_id):

    session = SessionLocal()

    try:

        rows = (

            session.query(

                Nutrient.nutrient_code,

                Nutrient.display_name,

                FoodNutrient.nutrient_value,

                Nutrient.unit,

            )

            .join(

                FoodNutrient,

                Nutrient.id == FoodNutrient.nutrient_id,

            )

            .filter(

                FoodNutrient.food_id == food_id

            )

            .order_by(

                Nutrient.display_name

            )

            .all()

        )

        df = pd.DataFrame(

            rows,

            columns=[

                "Code",

                "Nutrient",

                "Value",

                "Unit",

            ],

        )

        df["Value"] = pd.to_numeric(
            df["Value"],
            errors="coerce",
        )

        return df

    finally:

        session.close()


# ==========================================================
# Serving Calculation
# ==========================================================

def calculate_serving(df, grams):

    result = df.copy()

    result["Per100g"] = result["Value"]

    result["Serving"] = (

        result["Value"] * grams / 100

    ).round(3)

    return result