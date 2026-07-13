import streamlit as st
from sqlalchemy import func

from database.database import SessionLocal
from database.models import (
    Food,
    Nutrient,
    FoodNutrient,
)


# ==========================================================
# Get All Foods
# ==========================================================

@st.cache_data(show_spinner=False)
def get_all_foods():

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
# Get Food By ID
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food(food_id: int):

    session = SessionLocal()

    try:

        food = (
            session.query(Food)
            .filter(Food.id == food_id)
            .first()
        )

        return food

    finally:
        session.close()


# ==========================================================
# Search Foods
# ==========================================================

@st.cache_data(show_spinner=False)
def search_foods(keyword: str):

    session = SessionLocal()

    try:

        foods = (
            session.query(Food)
            .filter(
                Food.food_name.ilike(f"%{keyword}%")
            )
            .order_by(Food.food_name)
            .all()
        )

        return foods

    finally:
        session.close()


# ==========================================================
# Food Groups
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food_groups():

    session = SessionLocal()

    try:

        groups = (
            session.query(Food.food_group)
            .distinct()
            .order_by(Food.food_group)
            .all()
        )

        return [
            g[0]
            for g in groups
            if g[0] is not None and g[0] != ""
        ]

    finally:
        session.close()


# ==========================================================
# Nutrients of a Food
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food_nutrients(food_id: int):

    session = SessionLocal()

    try:

        nutrients = (
            session.query(
                Nutrient.nutrient_code.label("code"),
                Nutrient.display_name.label("nutrient"),
                FoodNutrient.nutrient_value.label("value"),
                Nutrient.unit.label("unit"),
            )
            .join(
                FoodNutrient,
                Nutrient.id == FoodNutrient.nutrient_id,
            )
            .filter(
                FoodNutrient.food_id == food_id
            )
            .order_by(
                Nutrient.nutrient_name
            )
            .all()
        )

        return nutrients

    finally:
        session.close()


# ==========================================================
# Single Nutrient Value
# ==========================================================

@st.cache_data(show_spinner=False)
@st.cache_data(show_spinner=False)
def get_single_nutrient(food_id: int, nutrient_code: str):

    session = SessionLocal()

    try:

        row = (
            session.query(
                FoodNutrient.nutrient_value.label("value"),
                Nutrient.unit.label("unit"),
            )
            .join(
                Nutrient,
                Nutrient.id == FoodNutrient.nutrient_id,
            )
            .filter(
                FoodNutrient.food_id == food_id,
                Nutrient.nutrient_code == nutrient_code,
            )
            .first()
        )

        return row

    finally:
        session.close()


# ==========================================================
# Food Count
# ==========================================================

@st.cache_data(show_spinner=False)
def get_food_count():

    session = SessionLocal()

    try:

        count = session.query(Food).count()

        return count

    finally:
        session.close()


# ==========================================================
# Nutrient Count
# ==========================================================

@st.cache_data(show_spinner=False)
def get_nutrient_count():

    session = SessionLocal()

    try:

        count = session.query(Nutrient).count()

        return count

    finally:
        session.close()