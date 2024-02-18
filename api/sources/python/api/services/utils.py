###
    # Welcome to utils.py, this file contains all functions, tools etc, that's can be usefull for the entire project
###
from api.schemas.common import NON_NULLABLE_ATTRS_MOUNTAIN_PEAKS
from api.schemas.mountain_peaks import MountainPeaks
from typing import List, Dict


def all_attrs_are_valid(data: MountainPeaks) -> bool:
    for attr in NON_NULLABLE_ATTRS_MOUNTAIN_PEAKS:
        if attr == 'name':
            if not hasattr(data, attr) or getattr(data, attr) is None:
                return False
        else:
            if not hasattr(data.location, attr) or getattr(data.location, attr) is None:
                return False
    return True

def all_mountains_peaks_are_valid_for_data_init(data: List[Dict]) -> bool:
    for m_peak in data:
        m_peak_obj = MountainPeaks(**m_peak)
        if not all_attrs_are_valid(m_peak_obj):
            return False
    return True