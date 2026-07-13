import streamlit as st
import pandas as pd
import plotly.express as px

from services.food_service import (
    get_all_foods,
    get_food_nutrients,
)

from utils.export import dataframe_to_csv


# ==========================================================
# Nutrition Summary Codes (IFCT 2017)
# ==========================================================

SUMMARY_CODES = {
    "Energy": "enerc",
    "Protein": "protcnt",
    "Total Fat": "fatce",
    "Carbohydrate": "choavldf",
    "Dietary Fibre": "fibtg",
}


# ==========================================================
# Category Mapping
# ==========================================================

def nutrient_category(code):

    vitamins = {
        "vita", "vitc", "thia", "ribf", "nia",
        "pantac", "biot", "fol", "vitb6",
        "vitb12", "cartb", "carta"
    }

    minerals = {
        "ca", "fe", "mg", "p", "k", "na",
        "zn", "cu", "mn", "se", "cr", "mo",
        "i"
    }

    amino = {
        "ala","arg","asp","cys","glu","gly",
        "his","ile","leu","lys","met","phe",
        "pro","ser","thr","trp","tyr","val"
    }

    fatty = {
        "fatce",
        "fasat",
        "famono",
        "fapoly",
        "fatrn",
        "omega3",
        "omega6"
    }

    if code in vitamins:
        return "Vitamins"

    if code in minerals:
        return "Minerals"

    if code in amino:
        return "Amino Acids"

    if code in fatty:
        return "Fatty Acids"

    if code in [
        "enerc",
        "protcnt",
        "fatce",
        "choavldf",
        "fibtg",
        "water",
        "ash",
    ]:
        return "Macronutrients"

    return "Others"


# ==========================================================
# Get Nutrient Value
# ==========================================================

def get_value(df, nutrient_code):

    row = df[df["Code"] == nutrient_code]

    if row.empty:
        return "-", ""

    value = row.iloc[0]["Value"]

    if pd.isna(value):
        return "-", ""

    value = float(value)

    unit = row.iloc[0]["Unit"] or ""

    # IFCT stores Energy in kcal
    # Display as kJ

    if nutrient_code == "enerc":

        value *= 1

        unit = "kJ"

    if unit == "":
        return f"{value:.2f}", ""

    if unit == "kJ":
        return f"{value:.0f}", "kJ"

    return f"{value:.2f}", unit

# ==========================================================
# Food Details Page
# ==========================================================

def show_food_details():

    st.title("🥗 Food Details")

    st.markdown(
        """
Explore complete nutritional composition from the **Indian Food Composition Tables (IFCT 2017)**.

All nutrient values are expressed **per 100 g edible portion**.
"""
    )

    # ------------------------------------------------------
    # Load Foods
    # ------------------------------------------------------

    foods = get_all_foods()

    if not foods:
        st.error("No foods found.")
        return

    # ------------------------------------------------------
    # Food Selector
    # ------------------------------------------------------

    selected_food = st.selectbox(
        "🔍 Search / Select Food",
        foods,
        format_func=lambda x: f"{x.food_name} ({x.food_code})",
        key="food_selector",
    )

    if selected_food is None:
        return

    # ------------------------------------------------------
    # Food Information
    # ------------------------------------------------------

    st.divider()

    left, right = st.columns([3, 1])

    with left:

        st.header(selected_food.food_name)

        st.write(f"**Food Code:** {selected_food.food_code}")

        st.write(
            f"**Scientific Name:** "
            f"{selected_food.scientific_name or '-'}"
        )

        st.write(
            f"**Food Group:** "
            f"{selected_food.food_group or '-'}"
        )

    with right:

        st.info(
            """
**Source**

Indian Food Composition Tables (IFCT 2017)

ICMR – National Institute of Nutrition
"""
        )

    # ------------------------------------------------------
    # Load Nutrients
    # ------------------------------------------------------

    nutrients = get_food_nutrients(selected_food.id)

    if len(nutrients) == 0:

        st.warning("No nutrient values available.")

        return

    # ------------------------------------------------------
    # Convert to DataFrame
    # ------------------------------------------------------

    df = pd.DataFrame(
        [
            {
                "Code": n.code,
                "Nutrient": n.nutrient,
                "Value": float(n.value)
                if n.value is not None
                else None,
                "Unit": n.unit,
            }
            for n in nutrients
        ]
    )

    # Remove rows without names

    df = df.dropna(subset=["Nutrient"])

    # Fill blank units

    df["Unit"] = df["Unit"].fillna("")

    # Add Category

    df["Category"] = df["Code"].apply(
        nutrient_category
    )

    # ==========================================================
# Nutrition Summary
# ==========================================================

    st.divider()

    st.subheader("📊 Nutrition Summary")

    c1, c2, c3, c4, c5 = st.columns(5)

    value, unit = get_value(df, "enerc")
    c1.metric("⚡ Energy", f"{value} {unit}")

    value, unit = get_value(df, "protcnt")
    c2.metric("🥩 Protein", f"{value} {unit}")

    value, unit = get_value(df, "fatce")
    c3.metric("🧈 Total Fat", f"{value} {unit}")

    value, unit = get_value(df, "choavldf")
    c4.metric("🌾 Carbohydrate", f"{value} {unit}")

    value, unit = get_value(df, "fibtg")
    c5.metric("🥬 Fibre", f"{value} {unit}")


# ==========================================================
# Serving Size Calculator
# ==========================================================

    st.divider()

    st.subheader("🥣 Serving Size Calculator")

    serving = st.slider(
    "Serving Size (g)",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
)

    factor = serving / 100.0

    df["Serving Value"] = df["Value"] * factor

    st.caption(
    f"All nutrient values below correspond to **{serving} g** of edible portion."
)


# ==========================================================
# Macronutrient Distribution
# ==========================================================

    protein = (
        df.loc[df["Code"] == "protcnt", "Serving Value"].iloc[0]
        if not df.loc[df["Code"] == "protcnt"].empty
        else 0
    )

    fat = (
        df.loc[df["Code"] == "fatce", "Serving Value"].iloc[0]
        if not df.loc[df["Code"] == "fatce"].empty
        else 0
)

    carb = (
        df.loc[df["Code"] == "choavldf", "Serving Value"].iloc[0]
        if not df.loc[df["Code"] == "choavldf"].empty
        else 0
    )

    pie_df = pd.DataFrame(
        {
            "Macronutrient": [
                "Protein",
                "Fat",
                "Carbohydrate",
            ],
            "Amount": [
                protein,
                fat,
                carb,
            ],
        }
    )

    fig = px.pie(
        pie_df,
        values="Amount",
        names="Macronutrient",
        hole=0.45,
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ==========================================================
# Explore Nutrients
# ==========================================================

    st.divider()

    st.subheader("🔍 Explore Nutrients")

    col1, col2 = st.columns([2, 1])

    with col1:

        search = st.text_input(
            "Search Nutrient",
            placeholder="Protein, Calcium, Vitamin C, Iron...",
            key="nutrient_search",
        )

    with col2:

        category = st.selectbox(
            "Category",
            [
                "All",
                "Macronutrients",
                "Vitamins",
                "Minerals",
                "Amino Acids",
                "Fatty Acids",
                "Others",
            ],
            key="category_filter",
        )

    # ----------------------------------------------------------
    # Apply Filters
    # ----------------------------------------------------------

    filtered_df = df.copy()

    if category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] == category
        ]

    if search:

        filtered_df = filtered_df[
            filtered_df["Nutrient"]
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    # ----------------------------------------------------------
    # Sorting
    # ----------------------------------------------------------

    sort_option = st.radio(
        "Sort By",
        [
            "Nutrient Name (A-Z)",
            "Highest Value",
            "Lowest Value",
        ],
        horizontal=True,
    )

    if sort_option == "Nutrient Name (A-Z)":

        filtered_df = filtered_df.sort_values(
            by="Nutrient"
        )

    elif sort_option == "Highest Value":

        filtered_df = filtered_df.sort_values(
            by="Serving Value",
            ascending=False,
        )

    else:

        filtered_df = filtered_df.sort_values(
            by="Serving Value",
            ascending=True,
        )

    # ----------------------------------------------------------
    # Nutrient Statistics
    # ----------------------------------------------------------

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Nutrients",
        len(df),
    )

    c2.metric(
        "Visible Nutrients",
        len(filtered_df),
    )

    c3.metric(
        "Serving Size",
        f"{serving} g",
    )
# ==========================================================
# Top Nutrients Chart
# ==========================================================

    st.divider()

    st.subheader("📊 Top Nutrients")

    chart_df = filtered_df.copy()

    # Remove missing values
    chart_df = chart_df.dropna(subset=["Serving Value"])

    # Keep only positive values
    chart_df = chart_df[
        chart_df["Serving Value"] > 0
    ]

    # Take Top 15
    chart_df = chart_df.nlargest(
        15,
        "Serving Value",
    )

    if not chart_df.empty:

        fig = px.bar(
            chart_df,
            x="Serving Value",
            y="Nutrient",
            orientation="h",
            text="Serving Value",
            title=f"Top Nutrients ({serving} g)",
        )

        fig.update_layout(

            height=650,

            yaxis=dict(
                categoryorder="total ascending"
            ),

            margin=dict(
                l=30,
                r=20,
                t=50,
                b=20,
            ),
        )

        fig.update_traces(
            textposition="outside",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("No nutrients available for visualization.")


    # ==========================================================
    # Nutrient Table
    # ==========================================================

    st.divider()

    st.subheader("📋 Complete Nutrient Profile")

    display_df = filtered_df.copy()

    display_df["Serving Value"] = display_df[
        "Serving Value"
    ].round(4)

    display_df = display_df.rename(
        columns={
            "Serving Value": f"Value ({serving} g)",
        }
    )

    display_df = display_df[
        [
            "Nutrient",
            f"Value ({serving} g)",
            "Unit",
            "Category",
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=700,
    )

    st.caption(
        f"Showing {len(display_df)} nutrients."
    )

    # ==========================================================
# DOWNLOAD SECTION
# ==========================================================

    st.divider()

    st.subheader("📥 Export Data")

    csv = dataframe_to_csv(display_df)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"{selected_food.food_name.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:

        st.info(
            f"""
    Current Export

    Food : {selected_food.food_name}

    Rows : {len(display_df)}

    Serving : {serving} g
    """
        )

    # ==========================================================
    # QUICK INSIGHTS
    # ==========================================================

    st.divider()

    st.subheader("📌 Quick Insights")

    try:

        energy = float(
            df.loc[df["Code"] == "enerc", "Value"].iloc[0]
        )

    except:

        energy = None

    try:

        protein = float(
            df.loc[df["Code"] == "protcnt", "Value"].iloc[0]
        )

    except:

        protein = None

    try:

        fat = float(
            df.loc[df["Code"] == "fatce", "Value"].iloc[0]
        )

    except:

        fat = None

    try:

        carbohydrate = float(
            df.loc[df["Code"] == "choavldf", "Value"].iloc[0]
        )

    except:

        carbohydrate = None

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### Macronutrients")

        st.write(f"⚡ Energy : {energy if energy is not None else '-'} kcal")

        st.write(f"🥩 Protein : {protein if protein is not None else '-'} g")

        st.write(f"🧈 Fat : {fat if fat is not None else '-'} g")

        st.write(f"🌾 Carbohydrate : {carbohydrate if carbohydrate is not None else '-'} g")

    with c2:

        st.markdown("### Dataset")

        st.write(f"Food Code : **{selected_food.food_code}**")

        st.write(f"Food Group : **{selected_food.food_group}**")

        st.write(f"Nutrients Available : **{len(df)}**")

        st.write(f"Serving Size : **{serving} g**")

    # ==========================================================
    # CATEGORY SUMMARY
    # ==========================================================

    st.divider()

    st.subheader("📂 Nutrient Category Summary")

    category_summary = (
        df.groupby("Category")
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        category_summary,
        x="Category",
        y="Count",
        text="Count",
        title="Available Nutrients by Category",
    )

    fig.update_layout(
        height=420,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ==========================================================
    # DATA SOURCE
    # ==========================================================

    st.divider()

    st.info(
        """
    ### Indian Food Composition Tables (IFCT 2017)

    This application exclusively uses the **Indian Food Composition Tables (IFCT 2017)** published by the **ICMR – National Institute of Nutrition (NIN)**.

    ✔ No USDA data has been used.

    ✔ All nutrient values are taken from the IFCT database stored locally in MySQL.

    ✔ Values are expressed per **100 g edible portion**, with optional serving-size calculations available on this page.

    NutriIndia is intended as an educational and analytical tool for exploring Indian food composition data.
    """
    )

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.divider()

    st.caption(
        "NutriIndia • Indian Food Composition Explorer • IFCT 2017"
    )