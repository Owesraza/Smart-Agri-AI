import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config.settings import settings
from app.models.sql_models import Base

logger = logging.getLogger(__name__)

# Create Async Engine
connect_args = {"check_same_thread": False} if "sqlite" in settings.resolved_database_url else {}

engine = create_async_engine(
    settings.resolved_database_url,
    echo=False,
    connect_args=connect_args,
    poolclass=NullPool if "sqlite" in settings.resolved_database_url else None,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db():
    """Create all SQL tables and seed default users on startup."""
    try:
        # 1. Safeguard: Automatic snapshot backup of database on startup
        import shutil
        from pathlib import Path
        db_file = Path(__file__).resolve().parent.parent.parent / "smartagri.db"
        if db_file.exists() and db_file.stat().st_size > 0:
            bak_file = db_file.with_suffix(".db.backup")
            try:
                shutil.copy2(db_file, bak_file)
                logger.info(f"🛡️ Safeguard: Database backed up to {bak_file.name}")
            except Exception as e:
                logger.warning(f"Could not create DB backup: {e}")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"✅ SQL Database initialized ({settings.resolved_database_url})")

        # 2. Guarantee permanent existence of primary Farmer and Buyer accounts
        async with AsyncSessionLocal() as session:
            from app.models.sql_models import UserModel
            from app.authentication.jwt_handler import hash_password
            from sqlalchemy import select

            farmer_pwd = hash_password("Owais@144")
            buyer_pwd = hash_password("Password123!")

            # Permanent Farmer: Owais Bhati
            res_farmer = await session.execute(select(UserModel).where(UserModel.email == "ansarbhati92@gmail.com"))
            farmer = res_farmer.scalar_one_or_none()
            if not farmer:
                session.add(UserModel(
                    id="0728f989d06e459f8ffc4d6192e9d480",
                    full_name="Owais Bhati",
                    mobile_number="8421783786",
                    whatsapp_number="8421783786",
                    email="ansarbhati92@gmail.com",
                    password=farmer_pwd,
                    village="Pune",
                    district="Pune",
                    state="Maharashtra",
                    farm_size=5.0,
                    role="farmer",
                    is_active=True,
                ))

            # Permanent Buyer: Amit Sharma
            res_buyer = await session.execute(select(UserModel).where(UserModel.email == "amit.buyer@smartagri.com"))
            buyer = res_buyer.scalar_one_or_none()
            if not buyer:
                session.add(UserModel(
                    id="05eb3965c3d54e9d9d16ec536576113b",
                    full_name="Amit Sharma",
                    mobile_number="9123456780",
                    whatsapp_number="9123456780",
                    email="amit.buyer@smartagri.com",
                    password=buyer_pwd,
                    village="Nashik",
                    district="Nashik",
                    state="Maharashtra",
                    role="Buyer",
                    is_active=True,
                ))

            await session.commit()
            logger.info("🌱 Verified core system accounts (Owais Bhati & Amit Sharma)")

    except Exception as e:
        logger.error(f"❌ SQL Database initialization failed: {e}")
        raise


async def close_db_connection():
    """Close SQL database connection on shutdown."""
    await engine.dispose()
    logger.info("SQL database connection closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Dependency for database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
