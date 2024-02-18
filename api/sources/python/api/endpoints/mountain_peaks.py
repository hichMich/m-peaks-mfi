#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends, status as http_status
from api.models import Base
from api.schemas.mountain_peaks import (
    MountainPeaks,
    MountainPeakOnCreateResponse,
    MountainPeaksEntire,
    Location
)
from api.services.mountain_peaks import (
    add_mountain_peak,
    get_mountain_peaks_by_all,
    initialize_mountains_peaks,
    remove_mountain_peak_by_criteria,
    get_mountain_peak_by_location,
    update_mountain_peak
)
from api.dao.postgres_dao import get_engine, get_db
from api.exceptions import ServiceFunctionalException, ServiceTechnicalException
from typing import List
from uuid import UUID
from sqlalchemy.exc import NoResultFound


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
        response_model=List[MountainPeaksEntire],
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
async def get_all_mountain_peaks(db=Depends(get_db)) -> List[MountainPeaksEntire]:
    """
        Get all moutain peaks

        #### Parameters: 
        - db: SqlAlchemy session
        
        #### Returns:
        - List of MountainPeaksOnGetResponse
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


@router.post(
        '/mountain_peaks/init',
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
def init_data_with_mountains_peaks_sample(db=Depends(get_db)):
    """
        Initialize mountains peaks data.
        
        ##### Attention ! this endpoint is only for oneshot use, d'ont duplicate data.

        #### Parameters: 
        - db: SqlAlchemy session
    """
    try:
        initialize_mountains_peaks(db)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex


@router.delete(
        '/mountain_peaks',
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
def remove_a_mountain_peak_by_criteria(criteria: Location | str | UUID, db=Depends(get_db)):
    """
        Delete a moutain peak by criteria

        Criteria is the name or the uuid or the location of a mountain peak
        ### Attention ! the specified criteria must be exisiting in the db 

        #### Parameters: 
        - criteria: Location | str | UUID
        - db: SqlAlchemy session
    """
    try:
        remove_mountain_peak_by_criteria(criteria, db)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex


@router.get(
        '/mountain_peak/{longitude}/{latitude}/{altitude}',
        response_model=MountainPeaksEntire,
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
def get_a_mountain_peak_by_location(
    longitude: float,
    latitude: float,
    altitude: float,
    db=Depends(get_db)
) -> MountainPeaksEntire:
    """
        Get a moutain peak by location

        location is the triplet of (longitude, latitude, altitude) of a mountain peak

        #### Parameters: 
        - location: Location
        - db: SqlAlchemy session
    """
    try:
        location = Location(longitude=longitude, latitude=latitude, altitude=altitude)
        return get_mountain_peak_by_location(location, db)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except NoResultFound as ex:
        raise HTTPException(status_code=http_status.HTTP_204_NO_CONTENT, detail=str(ex.args[0]))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex


@router.put(
        '/mountain_peak/{uuid}',
        status_code=http_status.HTTP_200_OK,
        tags=['mountain_peaks']
)
def update_a_mountain_peak(
    uuid: UUID,
    data: MountainPeaks,
    db=Depends(get_db)
):
    """
        Update a moutain peak

        #### Parameters: 
        - uuid: UUID
        - data: MountainPeaks
        - db: Session
    """
    try:
        update_mountain_peak(uuid, data, db)
    except ServiceFunctionalException as ex:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(ex.msg))
    except ServiceTechnicalException as ex:
        logger.error(ex.msg)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex.msg))
    except Exception as ex:
        logger.error(f"Unknown exception: {ex}")
        raise ex
