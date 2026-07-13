import streamlit as st

# ==========================================================
# PAGE CONFIG (FIRST STREAMLIT COMMAND)
# ==========================================================

st.set_page_config(
    page_title="NutriIndia",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# COMPONENTS
# ==========================================================

from components.theme import load_theme
from components.sidebar import show_sidebar

from components.food_explorer import show_food_explorer
from components.food_details import show_food_details
from components.compare import show_compare
from components.nutrient import show_nutrient_explorer
from components.calculator import show_calculator
from components.dashboard import show_dashboard
from components.admin import show_admin

# ==========================================================
# SERVICES
# ==========================================================

from services.food_service import (
    get_all_foods,
    get_food_count,
    get_nutrient_count,
    get_food_groups,
)

# ==========================================================
# LOAD THEME
# ==========================================================

load_theme()

# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "food_id" not in st.session_state:
    st.session_state.food_id = None

# ==========================================================
# SIDEBAR
# ==========================================================

selected_page = show_sidebar()

if selected_page:
    st.session_state.page = selected_page

# ==========================================================
# HOME
# ==========================================================

if st.session_state.page == "Home":

    st.title("🥗 NutriIndia")

    st.markdown(
        """
### Indian Food Composition Explorer

Explore the **Indian Food Composition Tables (IFCT 2017)** published by
**ICMR – National Institute of Nutrition**.

Search foods, compare nutrients, calculate serving sizes,
explore dashboards and analyze nutrition data.
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🍎 Foods",
        get_food_count(),
    )

    c2.metric(
        "🧬 Nutrients",
        get_nutrient_count(),
    )

    c3.metric(
        "🥦 Food Groups",
        len(get_food_groups()),
    )

    st.divider()

    st.subheader("Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
- 🍛 Food Explorer
- 🥗 Food Details
- 🔬 Nutrient Explorer
- ⚖ Compare Foods
""")

    with col2:

        st.markdown("""
- 🥣 Serving Calculator
- 📈 Dashboard
- 📄 CSV Export
- ⚙ Admin Panel
""")

    st.divider()

    st.subheader("About IFCT")

    st.info(
        """
The **Indian Food Composition Tables (IFCT 2017)** contain nutrient
composition data for Indian foods.

This application uses only the IFCT database stored locally in MySQL.
No USDA or external nutrition datasets are used.
"""
    )

# ==========================================================
# PAGES
# ==========================================================

elif st.session_state.page == "Food Explorer":

    show_food_explorer()

elif st.session_state.page == "Food Details":

    show_food_details()

elif st.session_state.page == "Compare Foods":

    show_compare()

elif st.session_state.page == "Nutrient Explorer":

    show_nutrient_explorer()

elif st.session_state.page == "Serving Calculator":

    show_calculator()

elif st.session_state.page == "Dashboard":

    show_dashboard()

elif st.session_state.page == "Admin":

    show_admin()