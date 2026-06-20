import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal, init_db as create_tables, engine
from src.main import app
from src.models import User


@pytest_asyncio.fixture(scope="session")
async def init_db():
    await create_tables()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(engine.sync_engine.drop_all)


@pytest_asyncio.fixture(scope='function')
async def db(init_db) -> AsyncSession:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_client(db) -> AsyncClient:
    from src.database import get_db
    
    async def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def clear_table(db: AsyncSession):
    try:
        await db.execute(text("DELETE FROM users;"))
        await db.commit()
    except Exception:
        await db.rollback()


@pytest_asyncio.fixture
async def user(db: AsyncSession) -> User:
    user = User(name="John Doe")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
