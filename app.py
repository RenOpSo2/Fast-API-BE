from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Literal

app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="0.0.1"
)

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    """
    Endpoint Home Page Untuk Load Jinja Templates /templates/index.html
    """
    return templates.TemplateResponse(
            "index.html",  
        {
            "request": request,
            "server_status": "Active" 
        }
    )

@app.get("/help", response_class=HTMLResponse)
async def get_help_page() -> HTMLResponse:
    """
  Html Respon Bukan Jinja2Templates
    """
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

