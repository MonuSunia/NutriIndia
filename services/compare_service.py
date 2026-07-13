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

        foods = (
            session.query(Food)
            .order_by(Food.food_name)
            .all()
        )

        return foods

    finally:
        session.close()


# ==========================================================
# Nutrient List
# ==========================================================

@st.cache_data(show_spinner=False)
def get_nutrients():

    session = SessionLocal()

    try:

        nutrients = (
            session.query(Nutrient)
            .order_by(Nutrient.display_name)
            .all()
        )

        return nutrients

    finally:
        session.close()


# ==========================================================
# Nutrient Matrix
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food_comparison(food_ids):

    session = SessionLocal()

    try:

        rows = (

            session.query(

                Food.food_name,

                Nutrient.display_name,

                Nutrient.nutrient_code,

                Nutrient.unit,

                FoodNutrient.nutrient_value,

            )

            .join(
                FoodNutrient,
                Food.id == FoodNutrient.food_id,
            )

            .join(
                Nutrient,
                Nutrient.id == FoodNutrient.nutrient_id,
            )

            .filter(
                Food.id.in_(food_ids)
            )

            .all()

        )

        data = pd.DataFrame(

            rows,

            columns=[

                "Food",

                "Nutrient",

                "Code",

                "Unit",

                "Value",

            ],

        )

        return data

    finally:

        session.close()


# ==========================================================
# Pivot Comparison Table
# ==========================================================

def comparison_table(df):

    table = df.pivot_table(

        index="Nutrient",

        columns="Food",

        values="Value",

        aggfunc="first",

    )

    table.reset_index(inplace=True)

    return table


# ==========================================================
# Summary Nutrients
# ==========================================================

SUMMARY_CODES = [

    "enerc",
    "protcnt",
    "fatce",
    "choavldf",
    "water",
    "fibtg",
    "ca",
    "fe",
    "zn",
    "vitc",

]


def summary_table(df):

    summary = df[df["Code"].isin(SUMMARY_CODES)]

    return comparison_table(summary)