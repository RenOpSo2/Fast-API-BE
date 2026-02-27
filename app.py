iimport os
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal

ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

class ServerStatus(BaseModel):
    message: str
    status: Literal["Development", "Production", "Staging"]
    version: str = "1.0.0"

app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="1.0.0"
)


@app.get("/", response_model=ServerStatus)
async def home_page() -> ServerStatus:
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
            <strong>Server Status</strong>
            <p>This server is built with FastAPI.</p>
            <p>Check the /docs endpoint for Swagger documentation.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

