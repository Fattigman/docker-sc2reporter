from db import *
from api.config import settings

"""
This module is used to interact with the sample collection in the database.
It contains all the CRUD functions for the sample collection.
"""
from .crud_base import CRUDBase
from .crud_significant_variants import significant_variants
from models import Sample

# Handling of the variants collection


class CRUDSamples(CRUDBase):
    """
    CRUD operations for the Samples collection.
    """

    def __init__(self):
        """
        Initialize CRUD operations for the Samples collection.
        """
        super().__init__(Sample, "sample")

    def filter_variant_pipeline(
        self, variants: list[str], filter_dict: dict = {}
    ) -> list[dict]:
        """
        Create a pipeline to filter variants.

        Args:
        - variants (list[str]): List of variants to filter.
        - filter_dict (dict, default={}): Additional filters.

        Returns:
        - list[dict]: The pipeline for filtering.
        """
        if filter_dict == {}:
            filter_dict = {"pangolin.type": {"$ne": "None"}}

        pipeline = [
            {"$match": filter_dict},
            {
                "$project": {
                    "sample_id": 1,
                    "nextclade": 1,
                    "pangolin": 1,
                    "collection_date": 1,
                    "selection_criterion": 1,
                    "qc": 1,
                    "sex": 1,
                    "mlu": 1,
                    "age": 1,
                    "Ct": 1,
                    "lab": 1,
                    "time_added": 1,
                    "variants": {
                        "$filter": {
                            "input": "$variants",
                            "as": "variant",
                            "cond": {"$in": [f"$$variant.aa", variants]},
                        }
                    },
                }
            },
        ]
        return pipeline

    async def get_samples(self, advanced_search: bool = False):
        """
        Retrieve samples, optionally using advanced search.

        Args:
        - advanced_search (bool, default=False): Whether to use advanced search.

        Returns:
        - list[dict]: List of samples.
        """
        if not advanced_search:
            variants = await significant_variants.get()
            variants = variants[0]["variants"]
            pipeline = self.filter_variant_pipeline(variants)
            # Filter out variants that are not in VARIANTS OF BIOLOGICAL SIGNIFICANCE

            cursor = db.sample.aggregate(pipeline)
        else:
            cursor = db.sample.find()
        docs = [parse_json(x) for x in await cursor.to_list(None)]
        return docs

    # Get samples associated with a specific type
    async def get_pangotype_samples(self, pangolin: str):
        """
        Retrieve samples associated with a specific pangolin type.

        Args:
        - pangolin (str): The pangolin type.

        Returns:
        - list[dict]: List of samples.
        """
        variants = await significant_variants.get()
        variants = variants[0]["variants"]
        pipeline = self.filter_variant_pipeline(variants, {"pangolin.type": pangolin})
        curr = db.sample.aggregate(pipeline)
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def get_variant_samples(self, variant: str):
        """
        Retrieve samples associated with a specific variant.

        Args:
        - variant (str): The variant.

        Returns:
        - list[dict]: List of samples.
        """
        variants = await significant_variants.get()
        variants = variants[0]["variants"]
        pipeline = self.filter_variant_pipeline(variants, {"variants.aa": variant})
        curr = db.sample.aggregate(pipeline)
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def get_nextclade_samples(self, nextclade: str):
        """
        Retrieve samples associated with a specific nextclade.

        Args:
        - nextclade (str): The nextclade.

        Returns:
        - list[dict]: List of samples.
        """
        curr = db.sample.find({"nextclade": nextclade})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def get_selection_criterions(self):
        """
        Retrieve selection criterions.

        Returns:
        - list: List of selection criterions.
        """
        curr = db.sample.aggregate(
            [
                {
                    "$group": {
                        "_id": {
                            "selection_criterion": "$selection_criterion",
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "selection_criterion": "$_id.selection_criterion",
                    }
                },
            ]
        )
        docs = [parse_json(x) for x in await curr.to_list(None)]
        docs = flatten([[doc[key] for key in doc if doc[key] != None] for doc in docs])
        return docs

    async def group_by_samples(self, selection_criterion: list = []):
        """
        Group samples by selection criterion.

        Args:
        - selection_criterion (list, default=[]): List of selection criterions.

        Returns:
        - list[dict]: List of grouped samples.
        """
        if selection_criterion == []:
            selection_criterion = await self.get_selection_criterions()
        curr = db.sample.aggregate(
            [
                {
                    # Group by pangolin type, selection criterion and selection_criterion
                    "$group": {
                        "_id": {
                            "pangolin": "$pangolin.type",
                            "date": "$collection_date",
                            "selection_criterion": "$selection_criterion",
                        },
                        "pango_count": {"$sum": 1},
                    },
                },
                {
                    # flatten the _id field
                    "$project": {
                        "pangolin": "$_id.pangolin",
                        "date": "$_id.date",
                        "pango_count": 1,
                        "selection_criterion": "$_id.selection_criterion",
                        "_id": 0,
                    }
                },
                {
                    # convert date to datetime
                    "$addFields": {
                        "date": {
                            "$dateToString": {"format": "%Y-%m-%d", "date": "$date"}
                        }
                    }
                },
                {
                    # filter out where "date" is "None"
                    "$match": {"pangolin": {"$ne": "None"}}
                },
                {
                    # filter by selection_criterion
                    "$match": {"selection_criterion": {"$in": selection_criterion}}
                },
                {
                    # Remove selection_criterion and group again
                    "$group": {
                        "_id": {
                            "pangolin": "$pangolin",
                            "date": "$date",
                        },
                        "pango_count": {"$sum": "$pango_count"},
                    }
                },
                {
                    # flatten the _id field
                    "$project": {
                        "pangolin": "$_id.pangolin",
                        "date": "$_id.date",
                        "pango_count": 1,
                        "_id": 0,
                    }
                },
                {
                    # sort by date
                    "$sort": {"date": 1}
                },
            ]
        )
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs

    async def get_general_stats(self):
        """
        Retrieve general statistics.

        Returns:
        - dict: Dictionary containing general statistics.
        """

        curr = db.sample.aggregate(
            [
                {
                    "$group": {
                        "_id": {
                            "sample_name": "$qc.qc_pass",
                        },
                        "passed_qc_samples": {"$sum": 1},
                    }
                },
                {
                    # filter out where sample_name is "FALSE"
                    "$match": {"_id.sample_name": {"$ne": "FALSE"}}
                },
                {  # Flatten the _id field
                    "$project": {
                        "_id": 0,
                        "passed_qc_samples": 1,
                    }
                },
            ]
        )
        docs = await curr.to_list(None)
        qc_samples = docs[0]["passed_qc_samples"]

        curr = db.sample.distinct("pangolin.type")
        unique_pangos = await curr
        unique_pangos = len([x for x in unique_pangos if x != "None"])

        curr = db.variant.distinct("_id")
        unique_variants = await curr
        unique_variants = len([x for x in unique_variants])
        return {
            "passed_qc_samples": qc_samples,
            "unique_pangos": unique_pangos,
            "unique_mutations": unique_variants,
        }

    async def delete_samples(self, sample_names: list):
        """
        Delete samples based on their names.

        Args:
        - sample_names (list): List of sample names.

        Returns:
        - int: Number of deleted samples.
        """
        curr = await db.sample.delete_many({"sample_id": {"$in": sample_names}})
        curr = await db.consensus.delete_many({"sample_id": {"$in": sample_names}})
        curr = await db.depth.delete_many({"sample_id": {"$in": sample_names}})
        return curr.deleted_count


samples = CRUDSamples()


def flatten(l):
    """
    Flatten a list of lists.

    Args:
    - l (list): List of lists.

    Returns:
    - list: Flattened list.
    """
    return [item for sublist in l for item in sublist]
