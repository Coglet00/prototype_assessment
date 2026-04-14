# prototype_assessment
An Asessment test for CREATE AI Intern

Backend - Fast API 

Storage - Google Sheets API 

Datasets - Creator Data and Campaign Data ( Fake) 

AI layer -  Pretrained sentence transformer (similarity search - cosine similarity) 

Custom matchscore =  recommends creators with high popularity and lower cost per post for campaign

Match score formula : A match score is computed for each, which combines the similarity score with other metrics (follower count, impressions, etc.) using a weighted formula. This ensures relevance isn't just about semantic match but also considers popularity, engagement, and cost

Frontend UI - Streamlit 


