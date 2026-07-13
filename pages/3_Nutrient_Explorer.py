import streamlit as st
import pandas as pd
import plotly.express as px

from services.nutrient_service import (
    get_all_nutrients,
    get_top_foods,
    get_average_value,
    get_max_value,
    get_min_value,
)

from utils.export import dataframe_to_csv


st.set_page_config(
    page_title="Nutrient Explorer",
    page_icon="🧪",
    layout="wide",
)


# ==========================================================
# Header
# ==========================================================

st.title("🧪 Nutrient Explorer")

st.markdown(
    """
Explore every nutrient available in the **Indian Food Composition Tables (IFCT 2017)**.

View the foods richest in any nutrient,
compare values and visualize the distribution.
"""
)

st.divider()


# ==========================================================
# Load Nutrients
# ==========================================================

nutrients = get_all_nutrients()

if len(nutrients) == 0:

    st.error("No nutrients found.")

    st.stop()


# ==========================================================
# Nutrient Selector
# ==========================================================

selected = st.selectbox(

    "Select Nutrient",

    nutrients,

    format_func=lambda x: x.display_name,

)


# ==========================================================
# Sidebar Options
# ==========================================================

with st.sidebar:

    st.header("Explorer Options")

    limit = st.slider(

        "Number of Foods",

        5,

        100,

        20,

    )

    order = st.radio(

        "Sort",

        [

            "Highest",

            "Lowest",

        ]

    )

    ignore_zero = st.checkbox(

        "Ignore Zero Values",

        value=True,

    )


descending = order == "Highest"


# ==========================================================
# Statistics
# ==========================================================

avg = get_average_value(selected.id)

mx = get_max_value(selected.id)

mn = get_min_value(selected.id)

c1, c2, c3 = st.columns(3)

c1.metric(

    "Average",

    "-" if avg is None else f"{float(avg):.2f} {selected.unit}",

)

c2.metric(

    "Maximum",

    "-" if mx is None else f"{float(mx):.2f} {selected.unit}",

)

c3.metric(

    "Minimum",

    "-" if mn is None else f"{float(mn):.2f} {selected.unit}",

)

st.divider()


# ==========================================================
# Food Ranking
# ==========================================================

rows = get_top_foods(

    selected.id,

    limit,

    descending,

    ignore_zero,

)

if len(rows) == 0:

    st.warning("No records found.")

    st.stop()


df = pd.DataFrame(

    rows,

    columns=[

        "Food",

        "Food Code",

        "Food Group",

        "Value",

    ],

)

df["Value"] = df["Value"].astype(float)


# ==========================================================
# Data Table
# ==========================================================

st.subheader(

    f"{order} {selected.display_name} Foods"

)

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)


# ==========================================================
# Plotly Bar Chart
# ==========================================================

fig = px.bar(

    df,

    x="Food",

    y="Value",

    hover_data=["Food Code"],

    title=f"{selected.display_name} ({selected.unit})",

)

fig.update_layout(

    xaxis_title="Food",

    yaxis_title=selected.unit,

    height=600,

)

st.plotly_chart(

    fig,

    use_container_width=True,

)


# ==========================================================
# Download CSV
# ==========================================================

csv = dataframe_to_csv(df)

st.download_button(

    "📥 Download CSV",

    csv,

    file_name=f"{selected.display_name}.csv",

    mime="text/csv",

)


# ==========================================================
# Information
# ==========================================================

st.info(

    f"""

**Nutrient**

{selected.display_name}

**Code**

{selected.nutrient_code}

**Unit**

{selected.unit}

**Source**

Indian Food Composition Tables (IFCT 2017)

"""

)