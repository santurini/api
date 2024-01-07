from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

import os
import json
from datetime import datetime
from easydict import EasyDict as edict

from app.models.item_model import Item
from app.handlers.item_handler import get_item, create_item
from app.handlers.key_handler import get_api_key

# initialize router to manage requests
router = APIRouter()

# initialize database on localhost: name -> fastapi, collection_name -> records
client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
collection = client[os.environ["MONGODB_DB_NAME"]][os.environ["MONGODB_COLLECTION"]]

# define retrieve endpoint following api.json specifications
@router.get("/api/v1/retrieve")
async def retrieve(date_from: str, date_to: str, api_key: str = Security(get_api_key)):
    
    # get mongodb pipelines to retrieve stats and logs
    pipeline, logs_pipeline = get_item(date_from, date_to)
    
    # run pipelines to obtain list of json outputs
    stats = await collection.aggregate(pipeline).to_list(None)
    logs = await collection.aggregate(logs_pipeline).to_list(None)
    
    # prepare response message 
    response = {
        "message": "Access granted!",
        "statistics": stats,
        "logs": logs,
        "status_code": 200
    }
    
    # convert datetime to string to be JSON compatible and read JSON for better output readability
    response = json.dumps(response, indent=2, default=str)
    response = json.loads(response)
    
    # return response in JSON format
    return JSONResponse(content=response, status_code=200)
    
@router.post("/api/v1/ingest")
async def ingest(item: Item, api_key: str = Security(get_api_key)):
    
    # create and insert JSON dict starting from {key, payload} item
    record = create_item(item)
    _ = await collection.insert_one(record)
    
    # prepare response message
    response = {
        "message": "Access granted!",
        "payload": record
    }
    
    # convert datetime to string to be JSON compatible and read JSON for better output readability
    response = json.dumps(response, indent=2, default=str)
    response = json.loads(response)
    
    # return response in JSON format
    return JSONResponse(content=response, status_code=200)