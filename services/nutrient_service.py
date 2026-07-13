from sqlalchemy import func, desc, asc

from database.database import SessionLocal
from database.models import Food, Nutrient, FoodNutrient

import streamlit as st


# ==========================================================
# Get All Nutrients
# ==========================================================

@st.cache_data(show_spinner=False)
def get_all_nutrients():

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
# Get Nutrient By Code
# ==========================================================

@st.cache_data(show_spinner=False)
def get_nutrient(code):

    session = SessionLocal()

    try:

        nutrient = (
            session.query(Nutrient)
            .filter(
                Nutrient.nutrient_code == code
            )
            .first()
        )

        return nutrient

    finally:
        session.close()


# ==========================================================
# Top Foods
# ==========================================================

@st.cache_data(show_spinner=False)
def get_top_foods(
    nutrient_id,
    limit=20,
    descending=True,
    ignore_zero=True,
):

    session = SessionLocal()

    try:

        query = (

            session.query(

                Food.food_name,

                Food.food_code,

                Food.food_group,

                FoodNutrient.nutrient_value,

            )

            .join(
                FoodNutrient,
                Food.id == FoodNutrient.food_id,
            )

            .filter(
                FoodNutrient.nutrient_id == nutrient_id
            )

        )

        if ignore_zero:

            query = query.filter(
                FoodNutrient.nutrient_value > 0
            )

        if descending:

            query = query.order_by(
                desc(
                    FoodNutrient.nutrient_value
                )
            )

        else:

            query = query.order_by(
                asc(
                    FoodNutrient.nutrient_value
                )
            )

        return query.limit(limit).all()

    finally:

        session.close()


# ==========================================================
# Average
# ==========================================================

@st.cache_data(show_spinner=False)
def get_average_value(nutrient_id):

    session = SessionLocal()

    try:

        value = (

            session.query(

                func.avg(
                    FoodNutrient.nutrient_value
                )

            )

            .filter(

                FoodNutrient.nutrient_id == nutrient_id

            )

            .scalar()

        )

        return value

    finally:

        session.close()


# ==========================================================
# Maximum
# ==========================================================

@st.cache_data(show_spinner=False)
def get_max_value(nutrient_id):

    session = SessionLocal()

    try:

        value = (

            session.query(

                func.max(
                    FoodNutrient.nutrient_value
                )

            )

            .filter(

                FoodNutrient.nutrient_id == nutrient_id

            )

            .scalar()

        )

        return value

    finally:

        session.close()


# ==========================================================
# Minimum
# ==========================================================

@st.cache_data(show_spinner=False)
def get_min_value(nutrient_id):

    session = SessionLocal()

    try:

        value = (

            session.query(

                func.min(
                    FoodNutrient.nutrient_value
                )

            )

            .filter(

                FoodNutrient.nutrient_id == nutrient_id

            )

            .scalar()

        )

        return value

    finally:

        session.close()