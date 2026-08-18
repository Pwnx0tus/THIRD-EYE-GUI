from fastapi import APIRouter
from pydantic import BaseModel
from main.ipcheck import check_ip

router = APIRouter(tags=["IP"])


class IPRequest(BaseModel):
    ip: str


@router.post("/ip")
async def ip_lookup(req: IPRequest):
    """
    IP address geolocation and ISP lookup using IPStack API.
    Returns country, region, city, lat/long, ISP, and language info.
    """
    ip = req.ip.strip()
    result = check_ip(ip)
    return {"status": "ok", "ip": ip, "data": result}
