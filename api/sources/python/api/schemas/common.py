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