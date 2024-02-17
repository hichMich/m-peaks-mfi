#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import Depends, BackgroundTasks, status as http_status
from api.models import Base
from api.schemas.mountain_peaks import MountainPeaks, MountainPeakOnCreateResponse
from api.services.mountain_peaks import add_mountain_peak
from api.dao.postgres_dao import get_engine, get_db
from api import context as ctx


router = APIRouter()
Base.metadata.create_all(bind=get_engine())

logger = logging.getLogger('mountain_peaks')


@router.post(
        '/mountain_peak',
        response_model=MountainPeakOnCreateResponse,
        status_code=http_status.HTTP_201_CREATED,
        tags=['mountain_peaks']
    )
async def create_mountain_peak(data: MountainPeaks, db=Depends(get_db)) -> MountainPeakOnCreateResponse:
    """
        Create a moutain peak
        ##### Attention ! The triplet (longitude, latitude, altitude) is unique
        
        #### Parameters: 
        - data: MountainPeaks
        - db: SqlAlchemy session
        
        #### Returns:
        - MountainPeakOnCreateResponse
    """
    mountain_peak_uuid = add_mountain_peak(data, db)
    return MountainPeakOnCreateResponse(uuid=mountain_peak_uuid)


