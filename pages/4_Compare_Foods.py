import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.compare_service import (
    get_foods,
    get_food_comparison,
    comparison_table,
    summary_table,
)

from utils.export import dataframe_to_csv


st.set_page_config(
    page_title="Compare Foods",
    page_icon="⚖️",
    layout="wide",
)


# ==========================================================
# HEADER
# ==========================================================

st.title("⚖️ Compare Foods")

st.markdown(
"""
Compare the nutritional composition of up to **five foods**
using the **Indian Food Composition Tables (IFCT 2017)**.

All values are expressed per **100 g edible portion**.
"""
)

st.divider()


# ==========================================================
# LOAD FOODS
# ==========================================================

foods = get_foods()

if len(foods) == 0:

    st.error("Database is empty.")

    st.stop()


# ==========================================================
# FOOD SELECTION
# ==========================================================

selected_foods = st.multiselect(

    "Choose up to 5 foods",

    foods,

    format_func=lambda x:
        f"{x.food_name} ({x.food_code})",

    max_selections=5,

)


if len(selected_foods) < 2:

    st.info("Select at least two foods.")

    st.stop()


food_ids = [

    food.id

    for food in selected_foods

]


# ==========================================================
# LOAD COMPARISON DATA
# ==========================================================

comparison_df = get_food_comparison(food_ids)

if comparison_df.empty:

    st.warning("No comparison data available.")

    st.stop()


comparison_df["Value"] = comparison_df["Value"].astype(float)


# ==========================================================
# FOOD OVERVIEW
# ==========================================================

st.subheader("Selected Foods")

cols = st.columns(len(selected_foods))

for col, food in zip(cols, selected_foods):

    with col:

        st.container(border=True)

        st.markdown(
            f"### {food.food_name}"
        )

        st.caption(food.food_code)

        st.write(
            f"**Group:** {food.food_group}"
        )

st.divider()

# ==========================================================
# COMPARISON TABLE
# ==========================================================

st.subheader("📊 Nutrient Comparison")

# Create pivot table
table = comparison_table(comparison_df)

# Search nutrient
search = st.text_input(
    "🔍 Search Nutrient",
    placeholder="Protein, Calcium, Iron..."
)

if search:

    table = table[
        table["Nutrient"]
        .str.contains(
            search,
            case=False,
            na=False,
        )
    ]

# Round numeric columns
display_table = table.copy()

for column in display_table.columns:

    if column != "Nutrient":

        display_table[column] = (
            pd.to_numeric(
                display_table[column],
                errors="coerce",
            )
            .round(2)
        )

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True,
    height=650,
)

st.caption(
    f"{len(display_table)} nutrients compared."
)

st.divider()


# ==========================================================
# QUICK SUMMARY
# ==========================================================

st.subheader("⚡ Nutrition Summary")

summary = summary_table(comparison_df)

summary_display = summary.copy()

for column in summary_display.columns:

    if column != "Nutrient":

        summary_display[column] = (
            pd.to_numeric(
                summary_display[column],
                errors="coerce",
            )
            .round(2)
        )

st.dataframe(
    summary_display,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ==========================================================
# INTERACTIVE CHARTS
# ==========================================================

st.subheader("📈 Visual Comparison")

# -----------------------------
# Nutrient Selector
# -----------------------------

available_nutrients = sorted(
    comparison_df["Nutrient"].dropna().unique().tolist()
)

selected_nutrient = st.selectbox(
    "Select a Nutrient",
    available_nutrients,
)

chart_df = comparison_df[
    comparison_df["Nutrient"] == selected_nutrient
].copy()

chart_df["Value"] = pd.to_numeric(
    chart_df["Value"],
    errors="coerce"
)

chart_df = chart_df.sort_values(
    "Value",
    ascending=False
)

# -----------------------------
# Bar Chart
# -----------------------------

fig_bar = px.bar(

    chart_df,

    x="Food",

    y="Value",

    text="Value",

    title=f"{selected_nutrient} Comparison",

)

fig_bar.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside",

)

fig_bar.update_layout(

    height=500,

    xaxis_title="Food",

    yaxis_title=selected_nutrient,

)

st.plotly_chart(

    fig_bar,

    use_container_width=True,

)

st.divider()


# ==========================================================
# RADAR CHART
# ==========================================================

st.subheader("🕸 Radar Comparison")

radar_codes = [

    "enerc",
    "protcnt",
    "fatce",
    "choavldf",
    "fibtg",
    "ca",
    "fe",
    "zn",

]

radar_df = comparison_df[
    comparison_df["Code"].isin(radar_codes)
].copy()

if not radar_df.empty:

    categories = radar_df["Nutrient"].unique().tolist()

    fig = go.Figure()

    for food in radar_df["Food"].unique():

        food_data = radar_df[
            radar_df["Food"] == food
        ]

        values = []

        for nutrient in categories:

            row = food_data[
                food_data["Nutrient"] == nutrient
            ]

            if row.empty:

                values.append(0)

            else:

                values.append(
                    float(
                        row.iloc[0]["Value"]
                    )
                )

        fig.add_trace(

            go.Scatterpolar(

                r=values,

                theta=categories,

                fill="toself",

                name=food,

            )

        )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

            )

        ),

        height=650,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

else:

    st.info(
        "Radar chart data unavailable."
    )

st.divider()

# ==========================================================
# STATISTICS
# ==========================================================

st.subheader("📊 Comparison Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Foods Compared",
    len(selected_foods),
)

c2.metric(
    "Nutrients",
    comparison_df["Nutrient"].nunique(),
)

c3.metric(
    "Food Groups",
    comparison_df["Food"].nunique(),
)

c4.metric(
    "Data Points",
    len(comparison_df),
)

st.divider()
# ==========================================================
# STATISTICS
# ==========================================================

st.subheader("📊 Comparison Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Foods Compared",
    len(selected_foods),
)

c2.metric(
    "Nutrients",
    comparison_df["Nutrient"].nunique(),
)

c3.metric(
    "Food Groups",
    comparison_df["Food"].nunique(),
)

c4.metric(
    "Data Points",
    len(comparison_df),
)

st.divider()

# ==========================================================
# CATEGORY VIEW
# ==========================================================

st.subheader("🧪 Explore Nutrient Categories")

categories = {

    "Proximate Composition": [

        "Water",

        "Protein",

        "Total Fat",

        "Available Carbohydrate",

        "Dietary Fibre",

        "Ash",

        "Energy",

    ],

    "Minerals": [

        "Calcium",

        "Iron",

        "Magnesium",

        "Phosphorus",

        "Potassium",

        "Sodium",

        "Zinc",

        "Copper",

        "Manganese",

    ],

    "Vitamins": [

        "Vitamin C",

        "Vitamin A",

        "Thiamine",

        "Riboflavin",

        "Niacin",

        "Vitamin B6",

        "Vitamin E",

        "Vitamin K",

        "Folate",

    ],

}

selected_category = st.selectbox(

    "Category",

    list(categories.keys())

)

category_df = comparison_df[

    comparison_df["Nutrient"].isin(

        categories[selected_category]

    )

]

if len(category_df):

    category_table = comparison_table(category_df)

    st.dataframe(

        category_table,

        hide_index=True,

        use_container_width=True,

    )

else:

    st.info(

        "No nutrients available in this category."

    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.success(

    """
Comparison completed successfully.

All nutrient values are obtained from the

Indian Food Composition Tables (IFCT 2017)

(ICMR–National Institute of Nutrition)

Values are expressed per 100 g edible portion.
"""
)