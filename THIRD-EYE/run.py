"""
THIRD-EYE - FastAPI Web GUI Launcher
Run: python run.py
"""
# pyrefly: ignore [missing-import]
import uvicorn

if __name__ == "__main__":
    print("\n  +======================================+")
    print("  |    THIRD-EYE - OSINT Web GUI        |")
    print("  |    http://localhost:8080             |")
    print("  +======================================+\n")
    uvicorn.run("api.server:app", host="127.0.0.1", port=8080, reload=True)
