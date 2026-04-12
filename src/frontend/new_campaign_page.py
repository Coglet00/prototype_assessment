from streamlit import session_state
import streamlit as st
from api_client import get_recommendations
from utils import go_to_existing_campaign, go_to_home
import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def new_campaign_page():
    st.subheader("New Campaign")

    campaign_name = st.text_input("Campaign Name", placeholder= 'Summer Collection Launch')
    campaign_code = st.text_input("Campaign Code", placeholder="E.g. CAMP12345")
    campaign_desc = st.text_area(" Campaign Description ", placeholder= 
        "Our brand is launching a new organic skincare line in Mumbai this August. "
        "We want Instagram beauty influencers and YouTube lifestyle creators who produce "
        "content in Hindi or English. The budget range is ₹4000–₹6000 per reel or video. "
        "The campaign aims to showcase product benefits, skincare routines, and authentic "
        "testimonials to build trust and excitement among health‑conscious young adults.", height=200)

    
    if st.button("Get Recommendations"):

        if campaign_name.strip() == "":
            st.warning("Please enter a campaign name.")
            return
        else:
            try:
                if detect(campaign_name) != "en":
                    st.warning("Caption is not in English, Only English Captions are supported")
                elif len(campaign_name) < 20:
                    st.warning("Caption must be more than 20 characters long")
            except LangDetectException:
                st.warning("Unable to detect language. Please enter a valid campaign name.")
                return
            
        if campaign_code.strip() == "":
            st.warning("Please enter a campaign code.")
            return

        if campaign_desc.strip() == "":
            st.warning("Please enter a campaign description.")
            return 
        
        recommendations = get_recommendations(campaign_name=None, campaign_desc=campaign_desc)
        
        if recommendations:
            st.subheader("Recommended Creators:")

            # Convert to DataFrame
            df = pd.DataFrame(recommendations)

            # Add a Tag column with default values
            df["Tag"] = "Unassigned"

            st.session_state["recommendations_df"] = df

    if "recommendations_df" in st.session_state:

        # Editable table: only Tag column is editable
        st.data_editor(
            st.session_state["recommendations_df"],
            num_rows="fixed",  # prevent adding/removing rows
            column_config={
                "Name": st.column_config.Column("Name", disabled=True),
                "Match Score": st.column_config.Column("Match Score", disabled=True),
                "Contact": st.column_config.Column("Contact", disabled=True),
                "Cost_Per_Post": st.column_config.Column("Cost_Per_Post", disabled=True),
                "Tag": st.column_config.SelectboxColumn(
                    "Tag",
                    options=["Shortlisted", "Backup", "Rejected", "Unassigned"],
                    default="Unassigned"
                )
            }
        )

    st.button("Go to Existing Campaign", on_click=go_to_existing_campaign)

    st.button("Go to Home", on_click=go_to_home)
        

