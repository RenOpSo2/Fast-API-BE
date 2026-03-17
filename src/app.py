from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
# from typing import Literal

from .database import engine, Base, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(
    title="Fast-API-BE",
    description="A properly structured FastAPI starter",
    version="0.0.3",
    lifespan=lifespan,
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
            "server_name": "Fast-API-BE",
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

@app.post("/users")
async def create_user(name: str, email: str, password: str):
    """
    Endpoint POST untuk membuat user
    """
    users = User(name=name, email=email, password=password)
    db.add(users)
    await db.commit()
    await db.refresh(users)
    return users

@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    await db.refresh(user)
    return user

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    users = users.scalars().all()
    return users

@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

