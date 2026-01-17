from app.api import article, subscriber, source
from contextlib import asynccontextmanager
from app.db.session import init_db, engine
from graph.prompts import load_prompts
from app.core.config import settings
import app.core.logger as logger
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 프롬프트 로드 (한 번만 실행)
    load_prompts()
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(article.router)
app.include_router(subscriber.router)
app.include_router(source.router)

@app.get("/health")
async def health_check():
    return {"message": "server is running..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT)