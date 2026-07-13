import streamlit as st

from services.food_service import (
    get_food_count,
    get_nutrient_count,
    get_food_groups,
)


# ==========================================================
# Recent Searches
# ==========================================================

def _add_recent_search(keyword: str):

    if not keyword:
        return

    keyword = keyword.strip()

    recent = st.session_state.get("recent_searches", [])

    if keyword in recent:
        recent.remove(keyword)

    recent.insert(0, keyword)

    st.session_state["recent_searches"] = recent[:5]


# ==========================================================
# Navigation Button
# ==========================================================

def nav_button(label, page_name, icon):

    if st.button(
        f"{icon}  {label}",
        use_container_width=True,
        key=f"nav_{page_name}",
    ):
        st.session_state.page = page_name
        st.rerun()


# ==========================================================
# Sidebar
# ==========================================================

def show_sidebar():

    with st.sidebar:

        # ------------------------------------------------------
        # Logo
        # ------------------------------------------------------

        st.markdown(
            """
# 🥗 NutriIndia

### Indian Food Composition Explorer
"""
        )

        st.caption("IFCT 2017 • ICMR-NIN")

        st.divider()

        # ------------------------------------------------------
        # Navigation
        # ------------------------------------------------------

        st.subheader("📂 Navigation")

        nav_button("Home", "Home", "🏠")

        nav_button(
            "Food Explorer",
            "Food Explorer",
            "🍛",
        )

        nav_button(
            "Food Details",
            "Food Details",
            "🥗",
        )

        nav_button(
            "Compare Foods",
            "Compare Foods",
            "⚖️",
        )

        nav_button(
            "Nutrient Explorer",
            "Nutrient Explorer",
            "🔬",
        )

        nav_button(
            "Serving Calculator",
            "Serving Calculator",
            "🥣",
        )

        nav_button(
            "Dashboard",
            "Dashboard",
            "📈",
        )

        nav_button(
            "Admin",
            "Admin",
            "⚙️",
        )

        st.divider()

        # ------------------------------------------------------
        # Database Status
        # ------------------------------------------------------

        st.subheader("📊 Database")

        try:

            foods = get_food_count()
            nutrients = get_nutrient_count()
            groups = len(get_food_groups())

            st.success("Connected")

            c1, c2 = st.columns(2)

            c1.metric(
                "Foods",
                foods,
            )

            c2.metric(
                "Nutrients",
                nutrients,
            )

            st.metric(
                "Food Groups",
                groups,
            )

        except Exception as e:

            st.error("Database Error")

            st.caption(str(e))

        st.divider()

        # ------------------------------------------------------
        # Quick Search
        # ------------------------------------------------------

        st.subheader("🔍 Quick Search")

        keyword = st.text_input(
            "Food Name",
            placeholder="Rice, Milk, Wheat...",
            key="sidebar_search_main",
        )

        if keyword:

            st.session_state.quick_search = keyword

            _add_recent_search(keyword)

        # ------------------------------------------------------
        # Session Information
        # ------------------------------------------------------

        st.divider()

        st.subheader("📈 Session")

        st.write(
            f"**Current Page:** {st.session_state.get('page','Home')}"
        )

        recent = st.session_state.get(
            "recent_searches",
            [],
        )

        st.write(
            f"**Recent Searches:** {len(recent)}"
        )

        if recent:

            with st.expander("Show Recent Searches"):

                for item in recent:

                    if st.button(
                        item,
                        key=f"recent_{item}",
                        use_container_width=True,
                    ):

                        st.session_state.quick_search = item

        # ------------------------------------------------------
        # About
        # ------------------------------------------------------

        st.divider()

        with st.expander("ℹ About"):

            st.markdown(
                """
### NutriIndia

Professional Nutrition Database

**Data Source**

Indian Food Composition Tables (IFCT 2017)

Published by

**ICMR – National Institute of Nutrition**

---

**Backend**

- MySQL
- SQLAlchemy

**Frontend**

- Streamlit

**Dataset**

- 542 Foods
- 176 Nutrients
"""
            )

        # ------------------------------------------------------
        # Footer
        # ------------------------------------------------------

        st.divider()

        st.caption("Version 2.0")

        st.caption("© 2026 NutriIndia")