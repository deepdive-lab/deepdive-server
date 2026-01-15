from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api import article, subscriber
from app.db.session import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(article.router)
app.include_router(subscriber.router)

@app.get("/health")
async def health_check():
    return {"message": "server is running..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT)