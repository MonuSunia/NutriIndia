import streamlit as st
from rapidfuzz import process


def search_box(food_names):

    query = st.text_input(
        "🔍 Search foods",
        placeholder="Rice, Wheat, Mango..."
    )

    if not query:
        return food_names

    matches = process.extract(
        query,
        food_names,
        limit=50
    )

    return [m[0] for m in matches]