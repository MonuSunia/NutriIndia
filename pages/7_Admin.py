import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import show_sidebar

# show_sidebar()
from services.admin_service import (
    get_database_stats,
    food_group_summary,
    search_food,
    clear_cache,
    health_check,
)

from services.food_service import get_all_foods
from utils.export import dataframe_to_csv

st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ NutriIndia Admin Panel")

st.markdown(
"""
Administrator tools for managing the
**Indian Food Composition Tables (IFCT 2017)** database.
"""
)

st.divider()

# ==========================================================
# DATABASE OVERVIEW
# ==========================================================

stats = get_database_stats()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Foods",
    f"{stats['foods']:,}"
)

c2.metric(
    "Nutrients",
    f"{stats['nutrients']:,}"
)

c3.metric(
    "Food-Nutrient Records",
    f"{stats['food_nutrients']:,}"
)

c4.metric(
    "Food Groups",
    f"{stats['food_groups']:,}"
)

st.divider()

st.subheader("Food Group Distribution")

groups = food_group_summary()

fig = px.pie(
    groups,
    names="Food Group",
    values="Foods",
    hole=0.45,
)

fig.update_layout(height=550)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

st.subheader("Database Health")

health = health_check()

c1, c2 = st.columns(2)

c1.metric(
    "Foods without nutrients",
    health["orphan_foods"]
)

c2.metric(
    "Duplicate Food Codes",
    health["duplicate_codes"]
)

if health["orphan_foods"] == 0:

    st.success("✓ Every food has nutrient values.")

else:

    st.warning("Some foods have no nutrient values.")

if health["duplicate_codes"] == 0:

    st.success("✓ No duplicate food codes.")

else:

    st.error("Duplicate food codes found.")

st.divider()

st.subheader("Search Database")

keyword = st.text_input(
    "Food Name"
)

if keyword:

    foods = search_food(keyword)

    if len(foods):

        df = pd.DataFrame(
            [
                {
                    "Food Code": f.food_code,
                    "Food": f.food_name,
                    "Food Group": f.food_group,
                }
                for f in foods
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No foods found.")

st.divider()

st.subheader("Cache Manager")

if st.button("🔄 Clear Streamlit Cache"):

    clear_cache()

    st.success("Cache cleared successfully.")

# ==========================================================
# EXPORT DATABASE
# ==========================================================

st.divider()
st.subheader("📤 Export Database")

foods = get_all_foods()

export_df = pd.DataFrame([
    {
        "Food Code": f.food_code,
        "Food Name": f.food_name,
        "Scientific Name": f.scientific_name,
        "Food Group": f.food_group,
    }
    for f in foods
])

csv = dataframe_to_csv(export_df)

st.download_button(
    "⬇ Download Foods CSV",
    csv,
    file_name="foods.csv",
    mime="text/csv",
)

st.success(f"{len(export_df)} foods ready for export.")

# ==========================================================
# DATABASE INSPECTOR
# ==========================================================

st.divider()
st.subheader("🔍 Database Inspector")

inspect_food = st.selectbox(
    "Select Food",
    foods,
    format_func=lambda x: f"{x.food_name} ({x.food_code})",
)

if inspect_food:

    st.write("### Basic Information")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Food Code**")
        st.write(inspect_food.food_code)

        st.write("**Food Group**")
        st.write(inspect_food.food_group)

    with c2:

        st.write("**Scientific Name**")
        st.write(
            inspect_food.scientific_name
            if inspect_food.scientific_name
            else "-"
        )

        st.write("**Database ID**")
        st.write(inspect_food.id)


# ==========================================================
# FOOD GROUP TABLE
# ==========================================================

st.divider()

st.subheader("📊 Food Group Statistics")

group_df = food_group_summary()

st.dataframe(
    group_df,
    hide_index=True,
    use_container_width=True,
)

fig = px.bar(
    group_df,
    x="Food Group",
    y="Foods",
    text="Foods",
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# MAINTENANCE
# ==========================================================

st.divider()

st.subheader("🛠 Maintenance")

col1, col2 = st.columns(2)

with col1:

    if st.button("Refresh Database"):

        st.cache_data.clear()

        st.success("Database refreshed successfully.")

with col2:

    if st.button("Reload Statistics"):

        st.cache_data.clear()

        st.rerun()


# ==========================================================
# INFORMATION
# ==========================================================

st.divider()

with st.expander("ℹ Database Information"):

    st.markdown(f"""

### Database

**Name**

nutriindia

**Tables**

- foods
- nutrients
- food_nutrients

**Foods**

{stats['foods']}

**Nutrients**

{stats['nutrients']}

**Food Nutrient Records**

{stats['food_nutrients']}

**Food Groups**

{stats['food_groups']}

**Source**

Indian Food Composition Tables (IFCT 2017)

ICMR – National Institute of Nutrition

""")
    

st.divider()

st.success(
"""
Admin Panel Loaded Successfully

✔ Database Connected

✔ Cache Working

✔ Inspector Ready

✔ Export Ready

✔ IFCT Database Active
"""
)