import sys, os
from api.config import settings
import asyncio
import motor
from .db import db
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

"""
Run when backend api starts
Checks if all collections exists in the database
Will create significant_variants, and user collection if they do not exist
"""


async def get_collections(db):
    collections = await db.list_collection_names()
    return collections


async def startup_db():
    print("Running startup_db")
    collections = await get_collections(db)
    # Checks if all collections exists in the database
    if "users" not in collections:
        print("User collection does not exist, creating...")
        hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(
            settings.ADMIN_PASSWORD
        )
        collection = db.users
        try:
            collection.insert_one(
                {
                    "_id": settings.ADMIN_USERNAME,
                    "username": settings.ADMIN_USERNAME,
                    "password": hashed_password,
                    "email": settings.ADMIN_EMAIL,
                    "fullname": settings.ADMIN_FULLNAME,
                    "disabled": False,
                    "scope": "admin",
                }
            )
            print(f"Users collection created with an user: {settings.ADMIN_USERNAME}.")
        except DuplicateKeyError:
            print("User already exists in the database")
    if "significant_variants" not in collections:
        print("Significant variants collection does not exist, creating...")
        collection = db.significant_variants
        collection.insert_one(
            {
                "_id": "significant_variants",
                "variants": settings.VARIANTS_OF_BIOLOGICAL_SIGNIFICANCE,
                "pango_lineages": settings.PANGO_LINEAGES_OF_CONCERN,
                "positions": settings.POSITIONS_OF_BIOLOGICAL_SIGNIFICANCE,
            }
        )
        print("Significant variants collection created.")
    print("Startup_db finished")
