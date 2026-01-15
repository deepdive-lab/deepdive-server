"""
데이터베이스 세션을 관리하는 모듈
Dependency Injection을 통해 api 단부터 데이터베이스 세션 제공
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models import Base
from app.core.config import settings

# engine to connect to the database
# echo=True: SQLAlchemy가 내부적으로 생성하는 SQL 쿼리문과 파라미터를 콘솔에 로깅
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# sessionmaker to create a session for queries
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        # JPA의 ddl-auto=dupate와 동일한 역할
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()