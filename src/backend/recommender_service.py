import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np
import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets API client

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(r"src/credentials.json", scopes=scope)
client = gspread.authorize(creds)


# Load your Google Sheets data into pandas
# Assuming you already have gspread client set up
spreadsheet = client.open("Prototype_data")

creator_data = spreadsheet.worksheet("Creator_data").get_all_records()
campaign_data = spreadsheet.worksheet("Campaign_data").get_all_records()

df_creators = pd.DataFrame(creator_data)
df_campaigns = pd.DataFrame(campaign_data)

# Load pretrained sentence-transformer
model = SentenceTransformer("all-mpnet-base-v2")

# Function to encode creator profiles and cache the vectors for efficiency


def encode_creators():


    # Convert creator rows into descriptive text
    def creator_to_text(row):
        return f"{row['Platform']} {row['Creator_Niche']} influencer from {row['City']}, {row['Follower_count']} followers, engagement rate {row['Engagement_rate']}, charges {row['Cost_Per_Post']} per post"

    creator_profiles = df_creators.apply(creator_to_text, axis=1).tolist()

    # Encode creator profiles once
    creator_vecs = model.encode(creator_profiles, convert_to_tensor=True)

    return creator_vecs


def compute_final_score(similarity, follower_count, impressions, reach, profile_views, engagement_rate, cost_per_post):
    # Normalize each metric so they’re on comparable scales
    
    # Popularity signals (log scale to dampen very large numbers)
    followers_norm = np.log1p(follower_count) / 10
    impressions_norm = np.log1p(impressions) / 12
    reach_norm = np.log1p(reach) / 12
    views_norm = np.log1p(profile_views) / 12
    
    # Engagement rate is already a percentage string like "7.50%"
    engagement_norm = float(str(engagement_rate).replace("%","")) / 100.0
    
    # Cost efficiency: lower cost = higher score
    cost_norm = 1 / (1 + cost_per_post)
    
    # Weighted combination (tune weights as per business priority)
    final_score = (
        0.4 * similarity +        # semantic relevance
        0.2 * followers_norm +    # popularity
        0.1 * impressions_norm +  # visibility
        0.1 * reach_norm +        # audience size
        0.05 * views_norm +       # profile activity
        0.1 * engagement_norm +   # engagement quality
        0.05 * cost_norm          # cost efficiency
    )
    
    return final_score


def compute_relevance_score(campaign_name=None, campaign_desc=None):
    """
    If campaign_name is provided, fetch its brief from df_campaigns.
    If campaign_desc is provided, use it directly.
    """

    # Case 1: Existing campaign
    if campaign_name is not None:
        # Find the campaign row by name
        row = df_campaigns[df_campaigns["Campaign Name"] == campaign_name]
        if row.empty:
            print("No campaign found with that name.")
            return pd.DataFrame(columns=["Creator ID","Name","Relevance"])

        campaign_desc = row.iloc[0]["Campaign Brief"]

    # Case 2: New campaign
    elif campaign_desc is None:
        print("You must provide either a campaign_name or a campaign_desc.")
        return 

    creator_vecs = encode_creators()

    # Encode campaign brief
    campaign_vec = model.encode(campaign_desc, convert_to_tensor=True)


    # Compute similarity
    scores = util.cos_sim(campaign_vec, creator_vecs)[0].cpu().numpy()

    df_creators["Match Score"] = scores

    # Sort and show top 5
    top_creators = df_creators.sort_values("Match Score", ascending=False).head(5)

    final_scores = top_creators.apply(lambda row: compute_final_score(
        similarity=row["Match Score"],
        follower_count=row["Follower_count"],
        impressions=row["Impressions"],
        reach=row["Reach"],
        profile_views=row["Profile_views"],
        engagement_rate=row["Engagement_rate"],
        cost_per_post=row["Cost_Per_Post"]
    ), axis=1)

    top_creators["Final_Score"] = final_scores

    return top_creators
