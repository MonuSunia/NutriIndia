import streamlit as st

# ==========================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
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

# ==========================================================
# SERVICES
# ==========================================================

from services.food_service import (
    get_food_count,
    get_nutrient_count,
    get_food_groups,
)

# ==========================================================
# LOAD THEME
# ==========================================================

load_theme()

# ==========================================================
# SIDEBAR
# ==========================================================

show_sidebar()

# ==========================================================
# HOME PAGE
# ==========================================================

st.title("🥗 NutriIndia")

st.markdown(
    """
## Indian Food Composition Explorer

Welcome to **NutriIndia**, a professional nutrition analysis platform based entirely on the **Indian Food Composition Tables (IFCT 2017)** published by **ICMR – National Institute of Nutrition**.

Use the **navigation menu in the left sidebar** to explore foods, compare nutrients, calculate serving values, and analyze the nutrition database.
"""
)

st.divider()

# ==========================================================
# DATABASE METRICS
# ==========================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "🍎 Foods",
    get_food_count(),
)

col2.metric(
    "🧬 Nutrients",
    get_nutrient_count(),
)

col3.metric(
    "🥦 Food Groups",
    len(get_food_groups()),
)

st.divider()

# ==========================================================
# FEATURES
# ==========================================================

st.subheader("✨ Features")

left, right = st.columns(2)

with left:
    st.markdown(
        """
### Food Analysis

- 🍛 Browse Indian foods
- 🥗 View complete nutrient profiles
- 🔬 Explore nutrients
- ⚖ Compare multiple foods
"""
    )

with right:
    st.markdown(
        """
### Nutrition Tools

- 🥣 Serving size calculator
- 📈 Nutrition dashboard
- 📄 CSV export
- ⚙ Database administration
"""
    )

st.divider()

# ==========================================================
# ABOUT IFCT
# ==========================================================

st.subheader("📚 About IFCT 2017")

st.info(
    """
The **Indian Food Composition Tables (IFCT 2017)** are published by the
**ICMR – National Institute of Nutrition (NIN)**.

NutriIndia uses only the IFCT dataset stored locally in a SQLite database.
No USDA or other external nutrition datasets are used.
"""
)

st.divider()

# ==========================================================
# QUICK START
# ==========================================================

st.subheader("🚀 Quick Start")

st.markdown(
    """
Use the **left sidebar** to navigate to:

- 🍛 Food Explorer
- 🥗 Food Details
- 🔬 Nutrient Explorer
- ⚖ Compare Foods
- 🥣 Serving Calculator
- 📈 Dashboard
- ⚙ Admin
"""
)

st.success("✅ NutriIndia")