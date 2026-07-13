import streamlit as st


# ---------------------------------------------------------
# Food Group Mapping (optional)
# ---------------------------------------------------------

FOOD_GROUPS = {
    "1": "Cereals & Millets",
    "2": "Pulses & Legumes",
    "3": "Vegetables",
    "4": "Fruits",
    "5": "Milk & Milk Products",
    "6": "Nuts & Oil Seeds",
    "7": "Meat & Poultry",
    "8": "Fish & Seafood",
    "9": "Eggs",
    "10": "Fats & Oils",
    "11": "Sugars",
    "12": "Spices & Condiments",
    "13": "Beverages",
}


def get_food_group(group):

    if group is None:
        return "-"

    return FOOD_GROUPS.get(str(group), str(group))


# ---------------------------------------------------------
# Food Card
# ---------------------------------------------------------

def food_card(food):

    with st.container(border=True):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.subheader(food.food_name)

            st.caption(f"IFCT Code : {food.food_code}")

            st.write(
                f"**Food Group:** {get_food_group(food.food_group)}"
            )

            if food.scientific_name:

                st.caption(
                    f"*{food.scientific_name}*"
                )

        with col2:

            st.write("")

            st.write("")

            if st.button(
                "View Details",
                key=f"view_{food.id}",
                use_container_width=True,
            ):

                st.session_state.food_id = food.id

                st.switch_page("pages/2_Food_Details.py")