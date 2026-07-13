import streamlit as st
import pandas as pd
from sqlalchemy import func, desc

from database.database import SessionLocal
from database.models import Food, Nutrient, FoodNutrient


# ==========================================================
# Dashboard Statistics
# ==========================================================

@st.cache_data(show_spinner=False)
def get_dashboard_stats():

    session = SessionLocal()

    try:

        food_count = session.query(Food).count()

        nutrient_count = session.query(Nutrient).count()

        group_count = (
            session.query(Food.food_group)
            .distinct()
            .count()
        )

        datapoints = session.query(FoodNutrient).count()

        return {
            "foods": food_count,
            "nutrients": nutrient_count,
            "groups": group_count,
            "values": datapoints,
        }

    finally:

        session.close()


# ==========================================================
# Food Group Distribution
# ==========================================================

@st.cache_data(show_spinner=False)
def food_group_distribution():

    session = SessionLocal()

    try:

        rows = (

            session.query(

                Food.food_group,

                func.count(Food.id)

            )

            .group_by(Food.food_group)

            .all()

        )

        return pd.DataFrame(

            rows,

            columns=[

                "Food Group",

                "Foods",

            ],

        )

    finally:

        session.close()


# ==========================================================
# Top Foods by Nutrient
# ==========================================================

@st.cache_data(show_spinner=False)
def top_foods(nutrient_code, limit=10):

    session = SessionLocal()

    try:

        rows = (

            session.query(

                Food.food_name,

                Food.food_group,

                FoodNutrient.nutrient_value,

                Nutrient.unit,

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
                Nutrient.nutrient_code == nutrient_code
            )

            .order_by(
                desc(FoodNutrient.nutrient_value)
            )

            .limit(limit)

            .all()

        )

        return pd.DataFrame(

            rows,

            columns=[

                "Food",

                "Food Group",

                "Value",

                "Unit",

            ],

        )

    finally:

        session.close()


# ==========================================================
# Average Nutrient
# ==========================================================

@st.cache_data(show_spinner=False)
def average_nutrient(nutrient_code):

    session = SessionLocal()

    try:

        value = (

            session.query(

                func.avg(
                    FoodNutrient.nutrient_value
                )

            )

            .join(
                Nutrient,
                Nutrient.id == FoodNutrient.nutrient_id,
            )

            .filter(
                Nutrient.nutrient_code == nutrient_code
            )

            .scalar()

        )

        return value

    finally:

        session.close()