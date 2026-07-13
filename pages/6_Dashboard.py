import streamlit as st
import plotly.express as px

from services.dashboard_service import *

st.set_page_config(

    page_title="Dashboard",

    page_icon="📊",

    layout="wide",

)

st.title("📊 NutriIndia Dashboard")

st.markdown(

"""
Interactive analytics powered by

**Indian Food Composition Tables (IFCT 2017)**

"""

)

st.divider()

stats = get_dashboard_stats()

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

    "Food Groups",

    f"{stats['groups']:,}"

)

c4.metric(

    "Nutrient Values",

    f"{stats['values']:,}"

)

st.divider()

st.subheader("Food Group Distribution")

groups = food_group_distribution()

fig = px.pie(

    groups,

    names="Food Group",

    values="Foods",

    hole=.45,

)

fig.update_layout(

    height=600,

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

st.divider()

st.subheader("🏆 Top Foods")

nutrients = {

    "Energy":"enerc",

    "Protein":"protcnt",

    "Total Fat":"fatce",

    "Available Carbohydrate":"choavldf",

    "Calcium":"ca",

    "Iron":"fe",

    "Zinc":"zn",

    "Vitamin C":"vitc",

}

selected = st.selectbox(

    "Select Nutrient",

    list(nutrients.keys())

)

df = top_foods(

    nutrients[selected],

    15,

)

st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

)

fig = px.bar(

    df,

    x="Food",

    y="Value",

    color="Food Group",

    text="Value",

)

fig.update_layout(

    height=600,

)

fig.update_traces(

    texttemplate="%{text:.2f}",

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

st.divider()

st.subheader("Average Nutrient Values")

c1,c2,c3,c4 = st.columns(4)

avg_energy = average_nutrient("enerc")
avg_protein = average_nutrient("protcnt")
avg_fat = average_nutrient("fatce")
avg_carb = average_nutrient("choavldf")

c1.metric(

    "Energy",

    f"{avg_energy:.1f} kcal"

)

c2.metric(

    "Protein",

    f"{avg_protein:.2f} g"

)

c3.metric(

    "Fat",

    f"{avg_fat:.2f} g"

)

c4.metric(

    "Carbohydrate",

    f"{avg_carb:.2f} g"

)

st.divider()

st.success(

"""
Dashboard generated successfully.

✔ IFCT 2017 Database

✔ Interactive Charts

✔ SQL Powered

✔ Cached Queries

✔ Responsive Layout

"""
)