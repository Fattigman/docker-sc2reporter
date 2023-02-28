import sys, os
from api.config import settings
import asyncio
import motor
from .db import db


async def get_collections(db):

    collections = await db.list_collection_names()
    return collections

async def startup_db():
    print("Running startup_db")
    collections =  await get_collections(db)
    # Checks if all collections exists in the database
    if ['sample', 'matrix', 'consensus', 'variant', 'significant_variants', 'depth', 'users'] == collections:
        print("All collections exists in the database")
        return True
    print("Missing collections in the database")
    return False