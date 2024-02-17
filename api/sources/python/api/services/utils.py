###
    # Welcome to utils.py, this file contains all functions, tools etc, that's can be usefull for the entire project
###
from api.schemas.common import NON_NULLABLE_ATTRS_MOUNTAIN_PEAKS
from api.schemas.mountain_peaks import MountainPeaks

def all_attrs_are_valid(data: MountainPeaks) -> bool:
    for attr in NON_NULLABLE_ATTRS_MOUNTAIN_PEAKS:
        if not hasattr(data, attr) or getattr(data, attr) is None:
            return False
    return True
