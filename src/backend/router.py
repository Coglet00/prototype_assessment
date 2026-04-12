from src.backend.auth import get_creators, get_campaigns
from src.backend.recommender_service import compute_relevance_score

from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter(prefix="/recommend", tags=["recommend"])



@router.get("/campaigns")
def get_campaigns_data():
    return {"data": get_campaigns()}


class CampaignRequest(BaseModel):
    campaign_name: str | None = None
    campaign_desc: str | None = None
    

@router.post("/recommend")
def recommend_creators(request: CampaignRequest):
    top_creators = compute_relevance_score(
        campaign_name=request.campaign_name,
        campaign_desc=request.campaign_desc
    )
    return top_creators[["Name","Match Score","Contact","Cost_Per_Post"]].to_dict(orient="records")

