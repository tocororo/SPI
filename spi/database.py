import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DB = "sp_institution"
MONGO_URI = f"mongodb://10.16.64.196:27017/{MONGO_DB}"
MONGO_MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MONGO_MIN_CONNECTIONS = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def get_persons_collection():
    return db.client.get_collection("persons")


async def get_pids_collection():
    return db.client.get_collection("pids")


async def connect():
    """Connect to MONGO DB
    """
    db.client = AsyncIOMotorClient(str(MONGO_URI),
                                   maxPoolSize=MONGO_MAX_CONNECTIONS,
                                   minPoolSize=MONGO_MIN_CONNECTIONS)
    print(f"Connected to mongo at {MONGO_URI}")


async def close():
    """Close MongoDB Connection
    """
    db.client.close()
    print("Closed connection with MongoDB")

