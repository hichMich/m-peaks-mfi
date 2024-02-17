#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends, status as http_status
from api.models import Base
from api.schemas.mountain_peaks import MountainPeaks, MountainPeakOnCreateResponse
from api.services.mountain_peaks import add_mountain_peak, get_mountain_peaks_by_all
from api.dao.postgres_dao import get_engine, get_db
from api.exceptions import ServiceFunctionalException, ServiceTechnicalException
from api import context as ctx
from typing import List


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
    try:
        mountain_peak_uuid = add_mountain_peak(data, db)
        return MountainPeakOnCreateResponse(uuid=mountain_peak_uuid)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex


@router.get(
        '/mountain_peaks',
        response_model=List[MountainPeaks],
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
async def get_all_mountain_peaks(db=Depends(get_db)) -> list[MountainPeaks]:
    """
        Get all moutain peaks

        #### Parameters: 
        - db: SqlAlchemy session
        
        #### Returns:
        - List of MountainPeaks
    """
    try:
        return get_mountain_peaks_by_all(db)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex




