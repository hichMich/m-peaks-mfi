###
    # Welcome to common.py, this file contain all common configs, objects, enums etc
###

from pydantic import BaseModel
class ApiBaseModel(BaseModel):
    """
        This class is generic, and allows all general config for other API schemas
    """
    class Config:
        from_attributes=True

NON_NULLABLE_ATTRS_MOUNTAIN_PEAKS = [
    'longitude',
    'latitude',
    'altitude',
    'name',
]

MOUNTAINS_PEAKS_SAMPLE = [
    {
        "name": "Mount Everest",
        "location": {
            "latitude": 27.9881,
            "longitude": 86.9250,
            "altitude": 8848
            },
    },
    {
        "name": "K2", 
        "location": {
            "latitude": 35.8814,
            "longitude": 76.5136,
            "altitude": 8611
        }
    },
    {
        "name": "Kangchenjunga",
        "location": {
            "latitude": 27.7025,
            "longitude": 88.1467,
            "altitude": 8586
        }
    },
    {
        "name": "Lhotse",
        "location": {
            "latitude": 27.9616,
            "longitude": 86.9336,
            "altitude": 8516
        }
    },
    {
        "name": "Makalu",
        "location": {
            "latitude": 27.8894,
            "longitude": 87.0889,
            "altitude": 8485
        }
    },
    {
        "name": "Cho Oyu",
        "location": {
            "latitude": 28.0942,
            "longitude": 86.6608,
            "altitude": 8188
        }
    },
    {
        "name": "Dhaulagiri I",
        "location": {
            "latitude": 28.6965,
            "longitude": 83.7142,
            "altitude": 8167
        }
    },
    {
        "name": "Manaslu",
        "location": {
            "latitude": 28.5518,
            "longitude": 84.5597,
            "altitude": 8163
        }
    },
    {
        "name": "Nanga Parbat",
        "location": {
            "latitude": 35.2372,
            "longitude": 74.5896,
            "altitude": 8126
        }
    },
    {
        "name": "Annapurna I",
        "location": {
            "latitude": 28.5953,
            "longitude": 83.8203,
            "altitude": 8091
        }
    }
]

