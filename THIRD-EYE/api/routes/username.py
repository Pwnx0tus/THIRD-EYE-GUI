import asyncio
import json
# pyrefly: ignore [missing-import]
from fastapi import APIRouter
# pyrefly: ignore [missing-import]
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from main.username import check_username_on_site, load_sites_config
from main.instaemailfind import instafind as infind
from main.scrap import chess, instauser, gitinfo
from concurrent.futures import ThreadPoolExecutor, as_completed

router = APIRouter(tags=["Username"])


class UsernameRequest(BaseModel):
    username: str


@router.post("/username/stream")
async def username_stream(req: UsernameRequest):
    """
    Streams username OSINT results using Server-Sent Events (SSE).
    Each checked platform sends an event so the UI updates in real-time.
    """
    username = req.username.strip()

    async def event_generator():
        sites = load_sites_config()
        total = len(sites)
        checked = 0

        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(check_username_on_site, username, site_name, site_config): site_name
                for site_name, site_config in sites.items()
            }

            for future in as_completed(futures):
                site_name, result_flag, link = future.result()
                checked += 1
                progress = round((checked / total) * 100, 1)

                event_data = {
                    "site": site_name,
                    "found": result_flag,
                    "url": link,
                    "progress": progress,
                    "checked": checked,
                    "total": total,
                    "extras": {},
                }

                # Run extra scrapers for special sites
                if result_flag is True:
                    if site_name.lower() == "instagram":
                        try:
                            email_data = await loop.run_in_executor(executor, infind, username)
                            profile_data = await loop.run_in_executor(executor, instauser, username)
                            event_data["extras"]["instagram"] = {
                                "email_find": email_data,
                                "profile": profile_data,
                            }
                        except Exception as e:
                            event_data["extras"]["instagram"] = {"error": str(e)}
                    elif site_name.lower() == "chess.com":
                        try:
                            event_data["extras"]["chess"] = await loop.run_in_executor(executor, chess, username)
                        except Exception as e:
                            event_data["extras"]["chess"] = {"error": str(e)}
                    elif site_name.lower() == "github":
                        try:
                            event_data["extras"]["github"] = await loop.run_in_executor(executor, gitinfo, username)
                        except Exception as e:
                            event_data["extras"]["github"] = {"error": str(e)}

                yield f"data: {json.dumps(event_data)}\n\n"
                await asyncio.sleep(0)

        yield f"data: {json.dumps({'done': True, 'username': username})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
