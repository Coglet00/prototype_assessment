import streamlit as st


def go_to_new_campaign():
    st.session_state.pop("recommendations_df", None)  # Clear recommendations when switching pages
    st.session_state["page"] = "new_campaign_page"


def go_to_existing_campaign():
    st.session_state.pop("recommendations_df", None)  # Clear recommendations when switching pages
    st.session_state["page"] = "existing_campaign_page"


def go_to_home():
    st.session_state.pop("recommendations_df", None)  # Clear recommendations when switching pages
    st.session_state["page"] = "home"