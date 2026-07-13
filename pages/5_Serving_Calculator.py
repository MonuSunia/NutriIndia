import streamlit as st
import pandas as pd
import plotly.express as px

from services.serving_service import (
    get_foods,
    get_food_profile,
    calculate_serving,
)

from utils.export import dataframe_to_csv


st.set_page_config(
    page_title="Serving Size Calculator",
    page_icon="🥣",
    layout="wide",
)

st.title("🥣 Serving Size Calculator")

st.markdown(
"""
Calculate nutrient values for any serving size using
the **Indian Food Composition Tables (IFCT 2017)**.
"""
)

foods = get_foods()

selected_food = st.selectbox(

    "Choose Food",

    foods,

    format_func=lambda x: f"{x.food_name} ({x.food_code})",

)

grams = st.number_input(

    "Serving Size (g)",

    min_value=1,

    max_value=1000,

    value=100,

    step=5,

)

df = get_food_profile(selected_food.id)

if df.empty:

    st.warning("No nutrient values found.")

    st.stop()

result = calculate_serving(df, grams)

# ==========================================================
# NUTRITION SUMMARY
# ==========================================================

st.divider()

st.subheader(f"Nutrition Summary ({grams} g Serving)")


def nutrient_value(code):

    row = result[result["Code"] == code]

    if row.empty:
        return "-"

    value = float(row.iloc[0]["Serving"])
    unit = row.iloc[0]["Unit"]

    return value, unit


# --------------------------
# Energy
# --------------------------

energy = nutrient_value("enerc")

if energy != "-":

    energy_kcal = energy[0]
    energy_kj = energy_kcal * 4.184

    energy_text = (
        f"{energy_kcal:.1f} kcal\n"
        f"{energy_kj:.1f} kJ"
    )

else:

    energy_text = "-"


# --------------------------
# Protein
# --------------------------

protein = nutrient_value("protcnt")

protein_text = "-"

if protein != "-":

    protein_text = f"{protein[0]:.2f} {protein[1]}"


# --------------------------
# Fat
# --------------------------

fat = nutrient_value("fatce")

fat_text = "-"

if fat != "-":

    fat_text = f"{fat[0]:.2f} {fat[1]}"


# --------------------------
# Carbohydrate
# --------------------------

carb = nutrient_value("choavldf")

carb_text = "-"

if carb != "-":

    carb_text = f"{carb[0]:.2f} {carb[1]}"


# --------------------------
# Fibre
# --------------------------

fibre = nutrient_value("fibtg")

fibre_text = "-"

if fibre != "-":

    fibre_text = f"{fibre[0]:.2f} {fibre[1]}"


c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Energy",
    energy_text,
)

c2.metric(
    "Protein",
    protein_text,
)

c3.metric(
    "Total Fat",
    fat_text,
)

c4.metric(
    "Carbohydrate",
    carb_text,
)

c5.metric(
    "Dietary Fibre",
    fibre_text,
)

st.divider()

# ==========================================================
# CHART
# ==========================================================

st.subheader("Major Nutrients")

major_codes = [

    "protcnt",

    "fatce",

    "choavldf",

    "fibtg",

]

chart = result[

    result["Code"].isin(major_codes)

].copy()

fig = px.bar(

    chart,

    x="Nutrient",

    y="Serving",

    text="Serving",

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside",

)

fig.update_layout(

    height=450,

    xaxis_title="",

    yaxis_title="g",

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

st.divider()

# ==========================================================
# COMPLETE PROFILE
# ==========================================================

st.subheader("Complete Nutrient Profile")

search = st.text_input(

    "Search Nutrient",

    placeholder="Protein, Calcium, Iron ..."

)

display = result.copy()

if search:

    display = display[

        display["Nutrient"]

        .str.contains(

            search,

            case=False,

            na=False,

        )

    ]

display = display[

    [

        "Nutrient",

        "Per100g",

        "Serving",

        "Unit",

    ]

]

display.columns = [

    "Nutrient",

    "Per 100 g",

    f"{grams} g",

    "Unit",

]

st.dataframe(

    display,

    use_container_width=True,

    hide_index=True,

    height=650,

)

st.caption(

    f"{len(display)} nutrients"

)

st.divider()

# ==========================================================
# EXPORT
# ==========================================================

csv = dataframe_to_csv(display)

st.download_button(

    "📥 Download CSV",

    csv,

    file_name=f"{selected_food.food_code}_{grams}g.csv",

    mime="text/csv",

)

st.success(

    f"Nutrient values successfully calculated for a {grams} g serving."

)

st.info(

    """
Source:
Indian Food Composition Tables (IFCT 2017)

All original values are expressed per 100 g edible portion.
The serving-size values are calculated proportionally from the IFCT data.
"""
)