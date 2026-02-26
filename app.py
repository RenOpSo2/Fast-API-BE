from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Route
@app.get("/")
async def home_page():
    return {
    "message": "Server Is Activate",
    "status": "Development Server"
}

@app.get("/help", response_class=HTMLResponse)
async def help_page():
    return "<h1>This server was created by the FastAPI library and has been optimized in more depth</h1>"



