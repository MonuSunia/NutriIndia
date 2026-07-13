import streamlit as st
import pandas as pd
from components.sidebar import show_sidebar

show_sidebar()
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database.database import SessionLocal
from database.models import (
    Food,
    Nutrient,
    FoodNutrient,
)


# ==========================================================
# DATABASE STATISTICS
# ==========================================================

@st.cache_data(show_spinner=False)
def get_database_stats():

    session = SessionLocal()

    try:

        return {

            "foods":
                session.query(Food).count(),

            "nutrients":
                session.query(Nutrient).count(),

            "food_nutrients":
                session.query(FoodNutrient).count(),

            "food_groups":
                session.query(Food.food_group)
                .distinct()
                .count(),

        }

    finally:

        session.close()


# ==========================================================
# FOOD GROUPS
# ==========================================================

@st.cache_data(show_spinner=False)
def food_group_summary():

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
# FIND FOOD
# ==========================================================

@st.cache_data(show_spinner=False)
def search_food(keyword):

    session = SessionLocal()

    try:

        foods = (

            session.query(Food)

            .filter(

                Food.food_name.ilike(
                    f"%{keyword}%"
                )

            )

            .order_by(Food.food_name)

            .all()

        )

        return foods

    finally:

        session.close()


# ==========================================================
# DELETE CACHE
# ==========================================================

def clear_cache():

    st.cache_data.clear()

    return True


# ==========================================================
# DATABASE HEALTH
# ==========================================================

@st.cache_data(show_spinner=False)
def health_check():

    session = SessionLocal()

    try:

        orphan_foods = (

            session.query(Food)

            .filter(

                ~Food.nutrients.any()

            )

            .count()

        )

        duplicate_codes = (

            session.query(

                Food.food_code

            )

            .group_by(

                Food.food_code

            )

            .having(

                func.count(Food.id) > 1

            )

            .count()

        )

        return {

            "orphan_foods": orphan_foods,

            "duplicate_codes": duplicate_codes,

        }

    finally:

        session.close()