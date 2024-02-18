from api.dao.mountain_peaks import (
    create_mountain_peak,
    select_all_mountains_peaks,
    retrieve_mountain_peak_by_uuid,
    retrieve_mountain_peak_by_name,
    retrieve_mountain_peak_by_location,
    init_mountains_peaks,
    delete_mountain_peak_by_uuid,
    delete_mountain_peak_by_name,
    delete_mountain_peak_by_location,
)
from api.schemas.mountain_peaks import MountainPeaks, MountainPeaksEntire, Location
from api.services import utils
from api.schemas.common import MOUNTAINS_PEAKS_SAMPLE
from api import context as ctx
from api.exceptions import ServiceFunctionalException, ServiceTechnicalException
from fastapi import status as http_status
import logging
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID


logger = logging.getLogger('services.mountain_peaks')

def get_mountain_peaks_by_all(db: Session) -> List[MountainPeaksEntire]:
    """
        Get all moutain peaks

        Parameters: 
        - db: SqlAlchemy session

        Returns:
        - List[MountainPeaksEntire]: The list of mountain peaks
    """
    try:
        m_peaks = select_all_mountains_peaks(db)
        mountains_peaks = [ 
                MountainPeaksEntire(
                    uuid=m_peak.uuid,
                    name=m_peak.name,
                    location=Location(
                        longitude=m_peak.longitude,
                        latitude=m_peak.latitude,
                        altitude=m_peak.altitude
                    )
                ) for m_peak in m_peaks
            ]
        return mountains_peaks
    except ServiceTechnicalException as ex:
        raise ex


def add_mountain_peak(data: MountainPeaks, db: Session) -> UUID:
    """
        Create a moutain peak
        Attention ! The triplet (longitude, latitude, altitude) is unique

        Parameters: 
        - data: MountainPeaks
        - db: SqlAlchemy session

        Returns:
        - UUID: The uuid of the created montain peak
    """
    validated_data = utils.all_attrs_are_valid(data)
    if not validated_data:
        raise ServiceFunctionalException(
            msg=f"Error ! Please check the requestBody object {data}",
            code_status=http_status.HTTP_400_BAD_REQUEST
        ) 
    try:
        mountain_peak_uuid = create_mountain_peak(data, db)
        return mountain_peak_uuid
    except ServiceTechnicalException as ex:
        raise ex


def initialize_mountains_peaks(db: Session):
    """
        Initialize some moutains peaks
        Attention ! This service is for oneshot use, don't duplicate data !

        Parameters: 
        - db: SqlAlchemy session
    """
    validated_data = utils.all_mountains_peaks_are_valid_for_data_init(MOUNTAINS_PEAKS_SAMPLE)
    if not validated_data:
        raise ServiceFunctionalException(
            msg=f"Error ! Please check montain peaks sample {MOUNTAINS_PEAKS_SAMPLE}",
            code_status=http_status.HTTP_400_BAD_REQUEST
        )
    try:
        init_mountains_peaks(MOUNTAINS_PEAKS_SAMPLE, db)
    except ServiceTechnicalException as ex:
        raise ex


def remove_mountain_peak_by_criteria(criteria: str | UUID | Location,  db: Session):
    """
        Remove a mountain peak by criteria

        Criteria is the name or the uuid or the location of a mountain peak

        ### Attention ! The specified criteria must exist in the database.

        Parameters: 
        - db: SqlAlchemy session
        - criteria: str | UUID | Location
    """
    try:
        uuid_criteria = UUID(criteria)
        delete_mountain_peak_by_uuid(uuid_criteria, db)
    except ValueError:
        delete_mountain_peak_by_name(criteria, db)
    except AttributeError:
        if isinstance(criteria, Location):
            delete_mountain_peak_by_location(criteria, db)
    except ServiceTechnicalException as ex:
        raise ex
    

def get_mountain_peak_by_location(location: Location,  db: Session) -> MountainPeaksEntire:
    """
        get a mountain peak by location

        Location is the triplet (longitude, latitude, altitude) of a mountain peak

        ### Attention ! The specified location must exist in the database.

        Parameters: 
        - db: SqlAlchemy session
        - location: Location
    """
    try:
        if isinstance(location, Location):
            return retrieve_mountain_peak_by_location(location, db)
    except ServiceTechnicalException as ex:
        raise ex
    