from streamlit import session_state 
import streamlit as st
from api_client import get_recommendations, get_campaign_names
from utils import go_to_new_campaign, go_to_home
import pandas as pd


def existing_campaign_page():

    st.subheader("Existing Campaign")

    campaign_names = get_campaign_names()

    campaign_name = st.selectbox("Select a Campaign", campaign_names)

    

    if st.button("Get Recommendations"):
        
        recommendations = get_recommendations(campaign_name=campaign_name, campaign_desc=None)

        if recommendations:
            st.subheader("Recommended Creators:")

            # Convert to DataFrame
            df = pd.DataFrame(recommendations)

            # Add a Tag column with default values
            df["Tag"] = "Unassigned"

            st.session_state["recommendations_df"] = df
    
    if "recommendations_df" in st.session_state:
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
            
    st.button("Go to New Campaign", on_click=go_to_new_campaign)
        
    st.button("Go to Home", on_click=go_to_home)
        
        


