import os
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal

ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

class ServerStatus(BaseModel):
    message: str
    status: Literal["Development", "Production", "Staging"]
    version: str = "0.0.1"

app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="0.0.1"
)


@app.get("/", response_model=ServerStatus)
async def get_home_page() -> ServerStatus:
    """
    Mengembalikan status server dan informasi lingkungan saat ini. Digunakan sebagai titik akhir pemeriksaan kesehatan.
    """
    return ServerStatus(
        message="Server is Active",
        status=ENVIRONMENT
    )

@app.get("/help", response_class=HTMLResponse)
async def get_help_page():
    return """
    <html>
        <head><title>Help</title></head>
        <body>
            <h1>Server Status</h1>
            <p>This server is built with FastAPI.</p>
            <p>Check the /docs endpoint for Swagger documentation.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

