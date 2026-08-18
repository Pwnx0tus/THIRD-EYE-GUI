from fastapi import APIRouter
from pydantic import BaseModel
from validator.emails import email_check
from validator.firefox import firefox
from validator.hudson import hudson
from validator.paste import paste
from validator.instagram import instafind as insta_email_check

router = APIRouter(tags=["Email"])


class EmailRequest(BaseModel):
    email: str


@router.post("/email")
async def email_lookup(req: EmailRequest):
    """
    Aggregates all email-based OSINT:
    - Cross-platform email registration check (Gravatar, etc.)
    - Firefox account check
    - Hudson Rock breach data
    - Pastebin exposure check
    - Instagram association check
    """
    email = req.email.strip()
    result = {}

    result["platform_check"] = email_check(email)
    result["firefox"] = firefox(email)
    result["breach_data"] = hudson(email)
    result["pastebin"] = paste(email)
    result["instagram"] = insta_email_check(email)

    return {"status": "ok", "email": email, "data": result}
