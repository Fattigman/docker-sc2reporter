from db import *
from pydantic import BaseModel
from pydantic.generics import GenericModel
from abc import ABC
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD class for all models.
    This will handle all the basic CRUD operations.
    In order to create more specific models, inherit from this class.
    """

    def __init__(self, model: Type[BaseModel], collection_name: str):
        """
        Initialize the CRUD base with a model and collection name.

        Args:
        - model (Type[BaseModel]): The Pydantic model type.
        - collection_name (str): The name of the MongoDB collection.
        """
        self.model = model
        self.collection_name = collection_name

    async def get(self, query: Optional[any] = None) -> List[Dict]:
        """
        Retrieve documents from the collection based on a query.

        Args:
        - query (Optional[any], default=None): The query to filter documents.

        Returns:
        - List[Dict]: List of documents matching the query.
        """
        cursor = db[self.collection_name].find(query)
        docs = [parse_json(x) for x in await cursor.to_list(None)]
        return docs

    async def get_single(self, id: str, id_field: str = "_id") -> List[Dict]:
        """
        Retrieve a single document from the collection based on an ID.

        Args:
        - id (str): The ID of the document to retrieve.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - List[Dict]: List containing the retrieved document.
        """
        curr = db[self.collection_name].find({id_field: id})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def get_multiple(self, ids: List[str], id_field: str = "_id") -> List[Dict]:
        """
        Retrieve multiple documents from the collection based on a list of IDs.

        Args:
        - ids (List[str]): List of IDs of the documents to retrieve.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - List[Dict]: List of retrieved documents.
        """
        curr = db[self.collection_name].find({id_field: {"$in": ids}})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def create(self, obj_in: BaseModel) -> Any:
        """
        Insert a new document into the collection.

        Args:
        - obj_in (BaseModel): The Pydantic model instance to insert.

        Returns:
        - Any: The result of the insert operation.
        """
        obj_in = obj_in.dict()
        result = await db[self.collection_name].insert_one(obj_in)
        return result

    async def update(
        self, id: str, obj_in: BaseModel, id_field: str = "_id"
    ) -> Optional[str]:
        """
        Update a document in the collection based on an ID.

        Args:
        - id (str): The ID of the document to update.
        - obj_in (BaseModel): The Pydantic model instance with updated data.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - Optional[str]: The ID of the updated document or None if no document was updated.
        """
        obj_in = obj_in.dict()
        result = await db[self.collection_name].update_one(
            {id_field: id}, {"$set": obj_in}
        )
        return result.upserted_id

    async def patch(
        self,
        id: str,
        obj_in: BaseModel,
        patch_field: str,
        patch_value: Any,
        id_field: str = "_id",
    ) -> Optional[str]:
        """
        Update a specific field of a document in the collection based on an ID.

        Args:
        - id (str): The ID of the document to update.
        - obj_in (BaseModel): The Pydantic model instance with updated data.
        - patch_field (str): The name of the field to update.
        - patch_value (Any): The new value for the patch_field.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - Optional[str]: The ID of the updated document or None if no document was updated.
        """
        result = await db[self.collection_name].update_one(
            {id_field: id}, {"$set": {patch_field: patch_value}}
        )
        return result.upserted_id

    async def delete(self, id: str, id_field: str = "_id") -> Any:
        """
        Delete a document from the collection based on an ID.

        Args:
        - id (str): The ID of the document to delete.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - Any: The result of the delete operation.
        """
        result = await db[self.collection_name].delete_one({id_field: id})
        return result

    async def delete_multiple(self, ids: List[str], id_field: str = "_id") -> Any:
        """
        Delete multiple documents from the collection based on a list of IDs.

        Args:
        - ids (List[str]): List of IDs of the documents to delete.
        - id_field (str, default="_id"): The field name for the ID.

        Returns:
        - Any: The result of the delete operation.
        """
        result = await db[self.collection_name].delete_many({id_field: {"$in": ids}})
        return result

    async def delete_all(self) -> Any:
        """
        Delete all documents from the collection.

        Returns:
        - Any: The result of the delete operation.
        """
        result = await db[self.collection_name].delete_many({})
        return result
