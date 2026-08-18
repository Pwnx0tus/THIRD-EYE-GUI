from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import phone, username, email, ip

app = FastAPI(
    title="THIRD-EYE OSINT",
    description="Terminal-Based OSINT Toolkit — now with a Web GUI",
    version="1.0.0",
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routers
app.include_router(phone.router, prefix="/api")
app.include_router(username.router, prefix="/api")
app.include_router(email.router, prefix="/api")
app.include_router(ip.router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/index.html")
