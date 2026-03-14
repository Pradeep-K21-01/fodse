"""
backend/app/api/routes/lawyer.py
GET  /lawyer/recommend  — Recommend lawyer type based on legal issue.
GET  /lawyer/nearby     — Return legal aid centres (static for now).
"""

from fastapi import APIRouter, Query
from app.schemas.response import LawyerResponse

router = APIRouter()

# Static legal aid centres by city
LEGAL_AID_CENTRES = {
    "chennai": [
        {"name": "Tamil Nadu State Legal Services Authority", "phone": "044-25320482", "address": "High Court Buildings, Chennai"},
        {"name": "Chennai District Legal Services Authority", "phone": "044-25354957", "address": "Singaravelar Maligai, Chennai"},
    ],
    "mumbai": [
        {"name": "Maharashtra State Legal Services Authority", "phone": "022-22632406", "address": "High Court, Mumbai"},
    ],
    "delhi": [
        {"name": "Delhi State Legal Services Authority", "phone": "011-23386458", "address": "Patiala House Courts, New Delhi"},
    ],
    "default": [
        {"name": "National Legal Services Authority (NALSA)", "phone": "15100", "website": "nalsa.gov.in"},
        {"name": "Legal Aid Helpline", "phone": "15100", "note": "Toll-free, available nationwide"},
    ]
}


@router.get("/recommend", response_model=LawyerResponse, summary="Recommend lawyer type")
async def recommend_lawyer(
    query: str = Query(..., example="My husband is filing for divorce"),
):
    """
    Based on a legal situation description, recommends the right type of lawyer
    and nearest free legal aid resources.
    """
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    from ai.agents.lawyer_agent import run

    result = run(query)
    return LawyerResponse(
        specialization = result["specialization"],
        suggestion     = result["suggestion"],
        legal_aid      = result["legal_aid"],
    )


@router.get("/nearby", summary="Get nearby legal aid centres")
async def nearby_lawyers(
    city: str = Query(default="default", example="chennai"),
):
    """
    Returns legal aid centres for the given city.
    Falls back to national resources if city is not found.
    """
    city_key = city.lower().strip()
    centres  = LEGAL_AID_CENTRES.get(city_key, LEGAL_AID_CENTRES["default"])
    return {
        "city":    city,
        "centres": centres,
        "helpline": "15100",
        "note":    "All services are free for eligible citizens under NALSA.",
    }
