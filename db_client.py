from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient("mongodb://hldpzz:Teste123@localhost:27017/?authMechanism=DEFAULT")

db = client.yellowpages
collection_prospect = db.prospect
#client = boto3.client('dynamodb',region_name='sa-east-1')

collection_query = db.query


def getRandom():
    random_document = collection_query.aggregate([{"$sample": { "size": 1 } }])
    for n in random_document:
        return n
    
def tryInsert(document):
    current_phone = document['phone']
    if collection_prospect.find_one({'phone':current_phone})==None:
        collection_prospect.insert_one(document)
        return True
    else:
        return False



__all__ = ['getRandom', 'tryInsert','collection_query','collection_prospect']
