from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from prompts.agents.db_expert.models import Patient, Condition, Observation
import asyncio
import os
        
class Database:
    """
    Database connection and initialization utility
    """

    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None

    async def connect(self):
        """
        Connect to MongoDB and initialize Beanie
        """
        self.client = AsyncIOMotorClient(self.connection_string)

        # Initialize Beanie with our models
        await init_beanie(
            database=self.client[self.database_name],
            document_models=[Patient, Condition, Observation],
        )

    async def disconnect(self):
        """
        Disconnect from MongoDB
        """
        if self.client:
            self.client.close()

    async def get_database_info(self):
        """
        Get database information
        """
        if not self.client:
            return None

        db = self.client[self.database_name]
        collections = await db.list_collection_names()

        return {
            "database_name": self.database_name,
            "collections": collections,
            "connection_status": "connected",
        }


# Singleton instance for the application
database = None


async def init_database(connection_string: str, database_name: str) -> Database:
    """
    Initialize the database connection
    """
    global database
    database = Database(connection_string, database_name)
    await database.connect()
    return database


def get_database() -> Database:
    """
    Get the database instance
    """
    if database is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return database



_client = None
_db = None
_beanie_ready = False
_lock = asyncio.Lock()


async def ensure_db_initialized():
    global _client, _db, _beanie_ready

    if _beanie_ready:
        return _db

    async with _lock:
        if _client is None:
            _client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
            _db = _client[os.environ["DATABASE_NAME"]]

        if not _beanie_ready:
            await init_beanie(
                database=_db,
                document_models=[Patient, Condition, Observation],
            )
            _beanie_ready = True

    return _db