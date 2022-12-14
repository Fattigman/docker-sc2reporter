from db import *

from api.config import settings
#  Handling of the samples collection

# Get samples from the database
async def get_samples(advanced_search:bool = False):
    if not advanced_search:
        # Filter out variants that are not in VARIANTS OF BIOLOGICAL SIGNIFICANCE
        pipeline = [
            {
                '$project': {
                    'sample_id': 1,
                    'nextclade': 1,
                    'pangolin': 1,
                    'collection_date': 1,
                    'selection_criterion': 1,
                    'qc': 1,
                    'time_added': 1,
                    'variants': {
                        '$filter': {
                            'input': '$variants',
                            'as': 'variant',
                            'cond': {
                                '$in': [
                                    '$$variant.aa', settings.VARIANTS_OF_BIOLOGICAL_SIGNIFICANCE
                                ]
                            }
                    }
                }
            }
        }
        ]
        cursor =  db.sample.aggregate(pipeline)
    else:
        cursor =  db.sample.find()
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_single_sample(sample_id : str):
    
    curr =  db.sample.find({"sample_id": sample_id})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_multiple_samples(sample_ids: list):
    curr =  db.sample.find({"sample_id": {'$in': sample_ids}})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

# Get samples associated with a specific type
async def get_pangotype_samples(pangolin:str):
    curr =  db.sample.find({"pangolin.type": pangolin})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_variant_samples(variant:str):
    curr =  db.sample.find({"variants.id" : variant})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_nextclade_samples(nextclade:str):
    curr =  db.sample.find({"nextclade": nextclade})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs
def flatten(l):
    return [item for sublist in l for item in sublist]

async def get_selection_criterions():
    curr = db.sample.aggregate([
        {
            '$group': {
                '_id': {
                    'selection_criterion': '$selection_criterion',
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'selection_criterion': '$_id.selection_criterion',
            }
        }
    ])
    docs = [parse_json(x) for x in await curr.to_list(None)]
    docs =   flatten([[doc[key] for key in doc if doc[key] != None ] for doc in docs])
    return  docs



async def group_by_samples(selection_criterion: list = []) :
    if selection_criterion == []:
        selection_criterion = await get_selection_criterions()
    curr = db.sample.aggregate([
        {
            # Group by pangolin type, selection criterion and selection_criterion
            '$group': {
                '_id': {
                    'pangolin': '$pangolin.type',
                    'date': '$collection_date',
                    'selection_criterion': '$selection_criterion',
                },
                'pango_count': {
                    '$sum': 1
                },
                
            },
        },{
            # flatten the _id field
            '$project': {
                'pangolin': '$_id.pangolin',
                'date': '$_id.date',
                'pango_count': 1,
                'selection_criterion': '$_id.selection_criterion',
                '_id': 0
            }
        },{
            # convert date to datetime
            '$addFields': {
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$date'
                    }
                }
            }
        },{
            # filter out where "date" is "None"
            '$match': {
                'pangolin': {
                    '$ne': 'None'
                }
            }
        },{
        #filter by selection_criterion
            '$match': {
                'selection_criterion': {
                    '$in': selection_criterion
                    }
             }
        },{
            # Remove selection_criterion and group again
            '$group': {
                '_id': {
                    'pangolin': '$pangolin',
                    'date': '$date',
                },
                'pango_count': {
                    '$sum': '$pango_count'
                },
            }
        },{
            # flatten the _id field
            '$project': {
                'pangolin': '$_id.pangolin',
                'date': '$_id.date',
                'pango_count': 1,
                '_id': 0
            }
        },{
            # sort by date
            '$sort': {
                'date': 1
            }
        }

    ])
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_general_stats():
    curr = db.sample.aggregate([
        {
            '$group': {
                '_id': {
                    'sample_name': '$qc.qc_pass',
                },
                'passed_qc_samples': {
                    '$sum': 1
                },
            }
        },{ 
            #filter out where sample_name is "FALSE"
            '$match': {
                '_id.sample_name': {
                    '$ne': "FALSE"
                }
            }
        },{ #Flatten the _id field
            '$project': {
                '_id': 0,
                'passed_qc_samples': 1,
            }
        }
        ])
    docs = await curr.to_list(None)
    qc_samples = docs[0]['passed_qc_samples']

    curr = db.sample.distinct('pangolin.type')
    unique_pangos = await curr
    unique_pangos = len([x for x in unique_pangos if x != 'None'])

    curr = db.variant.distinct('_id')
    unique_variants = await curr
    unique_variants = len([x for x in unique_variants])
    return  {'passed_qc_samples':qc_samples,'unique_pangos':unique_pangos, 'unique_mutations':unique_variants}
# Delete samples

async def delete_single_sample(sample_id : str):
    await db.sample.delete_one({"sample_id": sample_id})

async def delete_multiple_samples(sample_ids: list):
    await db.sample.delete_many({"sample_id": {'$in': sample_ids}})