import os
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal

ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

class ServerStatus(BaseModel):
    message: str
    status: Literal ["Development", "Production", "Staging"]
    version: str = "0.0.1"

app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="0.0.1"
)


# Basic Route
@app.get("/")
async def home_page():
    return {
    "message": "Server is Activate",
    "status": ENVIRONMENT
}


@app.get("/help", response_class=HTMLResponse)
async def help_page():
    return """
    <html>
        <head><title>Hell</title></head>
        <body>
            <strong>Server Status</strong>
            <p>This server is built with FastAPI.</p>
            <p>Check the /docs endpoint for Swagger documentation.</p>
        </body>
    </html>
    """
