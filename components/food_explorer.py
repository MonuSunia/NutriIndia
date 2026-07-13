import streamlit as st
from components.sidebar import show_sidebar

show_sidebar()
from services.food_service import (
    get_all_foods,
    get_food_groups,
)

from components.searchbox import search_box


def show_food_explorer():

    st.title("🍎 Food Explorer")

    foods = get_all_foods()

    if not foods:
        st.warning("No foods found in the database.")
        return

    food_names = [food.food_name for food in foods]

    matched_names = search_box(food_names)

    groups = ["All"] + get_food_groups()

    selected_group = st.selectbox(
        "Food Group",
        groups,
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

    PAGE_SIZE = 20

    total_pages = max(
        1,
        (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE,
    )

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1,
    )

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    current_foods = filtered[start:end]

    st.write(f"Showing {len(current_foods)} of {len(filtered)} foods")

    for food in current_foods:

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.subheader(food.food_name)

                st.caption(food.food_group)

            with col2:

                if st.button(
                    "View",
                    key=f"food_{food.id}",
                ):

                    st.session_state.food_id = food.id

                    st.session_state.page = "Food Details"

                    st.rerun()