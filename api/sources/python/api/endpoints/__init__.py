#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.endpoints import root
router = APIRouter()
router.include_router(root.router)
