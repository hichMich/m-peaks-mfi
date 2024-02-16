#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from fastapi import APIRouter
from api import context as ctx


router = APIRouter()
logger = logging.getLogger('root')


@router.get('/version', tags=['api'])
async def version():
    return {'version': ctx.VERSION}


@router.get('/health', tags=['api'])
async def health_check():
    return {'version': ctx.VERSION}

