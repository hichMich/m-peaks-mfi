#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.endpoints import root, mountain_peaks
router = APIRouter()
router.include_router(root.router)
router.include_router(mountain_peaks.router)
