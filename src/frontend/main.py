import streamlit as st 
from new_campaign_page import new_campaign_page
from existing_campaign_page import existing_campaign_page
import time


st.title("Creator Recommendation System")

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state['page'] == "new_campaign_page":
    new_campaign_page()
    
if st.session_state['page'] == "existing_campaign_page":
    existing_campaign_page()

if st.session_state.page == "home":
    st.subheader("Enter Campaign Details")

    st.write("")
    st.write("")
    
    if st.button("New Campaign", width= "stretch"):
        with st.spinner("Loading..."):
            time.sleep(1)

            st.session_state['page'] = "new_campaign_page"
            st.rerun()

    st.markdown("OR", text_alignment="center")
    
    if st.button("Existing Campaign", width= "stretch"):
        with st.spinner("Loading..."):
            time.sleep(1)

            st.session_state['page'] = "existing_campaign_page"
            st.rerun()