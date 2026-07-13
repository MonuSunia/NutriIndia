import streamlit as st

def metric(label, value):

    st.metric(
        label=label,
        value=value
    )