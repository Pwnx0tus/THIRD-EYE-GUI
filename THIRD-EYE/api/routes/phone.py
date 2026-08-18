from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from main.Numbercheck import search_google, validate_phone_number, look, WhatsappInfo
from main.idcheck import instafind

router = APIRouter(tags=["Phone"])


class PhoneRequest(BaseModel):
    number: str
    numverify_key: Optional[str] = None


@router.post("/phone")
async def phone_lookup(req: PhoneRequest):
    """
    Aggregates all phone-based OSINT:
    - Google search results
    - Phone validation (carrier, country, line type)
    - WhatsApp & Telegram quick links
    - WhatsApp profile info
    - Instagram account status check
    """
    number = req.number.strip()
    result = {}

    result["google"] = search_google(number)
    result["validation"] = validate_phone_number(number, api_key=req.numverify_key)
    result["links"] = look(number)
    result["whatsapp"] = WhatsappInfo(number)
    result["instagram_check"] = instafind(number)

    return {"status": "ok", "number": number, "data": result}
