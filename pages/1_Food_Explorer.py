import streamlit as st

from services.food_service import (
    get_all_foods,
    get_food_groups
)
from components.sidebar import show_sidebar

show_sidebar()

from components.searchbox import search_box

st.title("🍎 Food Explorer")

foods = get_all_foods()

food_names = [f.food_name for f in foods]

matched_names = search_box(food_names)

groups = ["All"] + get_food_groups()

selected_group = st.selectbox(
    "Food Group",
    groups
)

filtered = []

for food in foods:

    if food.food_name not in matched_names:
        continue

    if (
        selected_group != "All"
        and food.food_group != selected_group
    ):
        continue

    filtered.append(food)

st.write(f"Foods Found: {len(filtered)}")

for food in filtered:

    with st.container(border=True):

        c1, c2 = st.columns([5, 1])

        with c1:
            st.subheader(food.food_name)
            st.caption(food.food_group)

        with c2:
            if st.button(
                "View",
                key=f"view_{food.id}"
            ):
                st.session_state.food_id = food.id

