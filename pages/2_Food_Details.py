import streamlit as st

from components.theme import load_theme
from components.sidebar import show_sidebar
from components.food_details import show_food_details

st.set_page_config(
    page_title="Food Details",
    page_icon="🥗",
    layout="wide",
)

load_theme()
show_sidebar()

show_food_details()