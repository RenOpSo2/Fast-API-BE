"""
FastAPI Backend Application
Main entry point for the REST API server with Jinja2 templating support.
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

from .database import engine, Base, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events:
    - On startup: Creates all database tables based on SQLAlchemy models
    - On shutdown: Cleanup (implicit via context manager exit)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="0.0.3",
    lifespan=lifespan,
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    """
    Home page endpoint.
    
    Renders the main index.html template with server information.
    
    Args:
        request: FastAPI Request object for template context
        
    Returns:
        TemplateResponse: Rendered index.html template
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "server_name": "Fast-API-BE",
            "server_status": "Active"
        }
    )


@app.get("/help", response_class=HTMLResponse)
async def get_help_page() -> HTMLResponse:
    """
    Help page endpoint.
    
    Returns raw HTML response (not using Jinja2 template).
    Provides information about the server and available documentation.
    
    Returns:
        HTMLResponse: Raw HTML help page
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


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all users from the database.
    
    Fetches all user records without any filtering or pagination.
    
    Args:
        db: AsyncSession dependency for database operations
        
    Returns:
        list: List of all User objects
        
    Example:
        GET /users
        Response: [{"id": 1, "name": "John", "email": "john@example.com"}, ...]
    """
    users = await db.execute(select(User))
    users = users.scalars().all()
    return users


@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific user by ID.
    
    Fetches a single user record from the database using the provided ID.
    
    Args:
        id: User ID to retrieve (path parameter)
        db: AsyncSession dependency for database operations
        
    Returns:
        User: User object matching the given ID
        
    Raises:
        HTTPException: 404 error if user is not found
        
    Example:
        GET /users/1
        Response: {"id": 1, "name": "John", "email": "john@example.com"}
    """
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

