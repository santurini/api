from fastapi import HTTPException, status

import random
from easydict import EasyDict as edict
from datetime import datetime, timezone

from app.models.item_model import Item

def get_item(date_from: str, date_to: str):
    
    # check if requests date format is correct
    date_format = "%Y-%m-%d %H:%M:%S"
    
    try:
        # Parse the string into a datetime object
        date_from = datetime.strptime(date_from, date_format)
        date_from = date_from.replace(tzinfo=timezone.utc)
        
        date_to = datetime.strptime(date_to, date_format)
        date_to = date_to.replace(tzinfo=timezone.utc)
    
    # raise Exception if date format does not match 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format, correct format is: YYYY-MM-DD hh:mm:ss (example: date_from=2024-01-05 13:25:12)",
        )

    # create pipeline with datetimes to extract stats per minute
    pipeline = [
    {
        '$match': {
            'time': {
                '$gte': date_from, 
                '$lt': date_to
            }
        }
    }, {
        '$group': {
            '_id': {
                'key': '$key', 
                'minute': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:00', 
                        'date': '$time'
                    }
                }
            }, 
            'total_response_time_ms': {
                '$sum': '$response_time'
            }, 
            'total_requests': {
                '$sum': 1
            }, 
            'total_errors': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$response_code', 500
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'key': '$_id.key', 
            'total_response_time_ms': '$total_response_time_ms', 
            'total_requests': '$total_requests', 
            'total_errors': '$total_errors', 
            'creation_datetime': '$_id.minute'
        }
    }, {
        '$sort': {
            'key': 1,
            'creation_datetime': 1
        }
    }]
    
    # create pipeline with datetimes to extract last 10 logs for time interval
    logs_pipeline = [
    {
        '$match': {
            'time': {
                '$gte': date_from, 
                '$lt': date_to
            }
        }
    }, {
        '$sort': {
            'time': -1
        }
    }, {
        '$limit': 10
    }, {
        '$project': {
            '_id': 0, 
            'key': 1, 
            'payload': 1, 
            'response_time': 1, 
            'response_code': 1, 
            'creation_datetime': '$time'
        }
    }]

    return pipeline, logs_pipeline

def create_item(item: Item):
    
    # create record to be stored
    record = {
        "key": item.key,
        "payload": item.payload,
        "response_time": int(random.uniform(10, 50)), # random response time between 10 and 50 ms
        "response_code": random.choices([200, 500], weights=[90, 10])[0], # 90% probability to be successfull
        "time": datetime.now(), # insertion datetime
    }
    
    return record