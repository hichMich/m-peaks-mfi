#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from fastapi import FastAPI
from core import endpoints

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from core import context as ctx
from core.models import Base

from core.dao.postgres_dao import get_engine

logger = logging.getLogger('main')

logging.getLogger('multipart.multipart').setLevel(logging.ERROR)

Base.metadata.create_all(bind=get_engine())

logger = logging.getLogger('main')
logging.getLogger('multipart.multipart').setLevel(logging.ERROR)
Base.metadata.create_all(bind=get_engine())

app = FastAPI(title='m-peaks-mfi api', description='Montain peaks API for MFI', version=ctx.VERSION, root_path=ctx.DEPLOYED_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info('Startup API')


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('Shutdown API')


app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
