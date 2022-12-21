from db import *
from pydantic import BaseModel
from pydantic.generics import GenericModel
from abc import ABC
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


"""
Genereic CRUD class for all models.
This will handle all the basic CRUD operations.
In order to create more specific models, inherit from this class.
"""
class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[BaseModel], collection_name: str):
        self.model = model
        self.collection_name = collection_name

    async def get(self, query: Optional[any] = None):
        print (self.collection_name)
        cursor =  db[self.collection_name].find(query)
        docs = [parse_json(x) for x in await cursor.to_list(None)]
        return (docs)

    async def get_single(self, id : str, id_field: str = "_id"):
        curr =  db[self.collection_name].find({id_field: id})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return  docs

    async def get_multiple(self, ids, id_field: str = "_id"):
        curr =  db[self.collection_name].find({id_field: {'$in': ids}})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return  docs

    async def create(self, obj_in: BaseModel, id_field: str = "_id"):
        obj_in = obj_in.dict()
        obj_in[id_field] = obj_in["sample_id"]
        result = await db[self.collection_name].insert_one(obj_in)
        return result
    
    async def update(self, id: str, obj_in: BaseModel, id_field: str = "_id"):
        # Returns None if no document was updated
        # else returns the _id of the updated document
        obj_in = obj_in.dict()
        result = await db[self.collection_name].update_one({id_field: id}, {"$set": obj_in})
        return result.upserted_id

    async def delete(self, id: str, id_field: str = "_id"):
        result = await db[self.collection_name].delete_one({id_field: id})
        return result
    
    async def delete_multiple(self, ids, id_field: str = "_id"):
        result = await db[self.collection_name].delete_many({id_field: {'$in': ids}})
        return result
    
    async def delete_all(self):
        result = await db[self.collection_name].delete_many({})
        return result