import requests
import streamlit as st


# Fetch your Vercel URL from Streamlit Secrets
BASE_URL = st.secrets["BACKEND_URL"]


def get_recommendations(campaign_name, campaign_desc):
    payload = {"campaign_name": campaign_name, "campaign_desc": campaign_desc}
    response = requests.post(f"{BASE_URL}/recommend/recommend", json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching recommendations:", response.text)
        return None

    
def get_campaign_names():
    response = requests.get(f"{BASE_URL}/recommend/campaigns")
    
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Error fetching campaign names:", response.text)
        return None
