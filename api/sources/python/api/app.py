#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from fastapi import FastAPI
from api import endpoints

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from api import context as ctx
from api.models import Base

from api.dao.postgres_dao import get_engine

logger = logging.getLogger('main')
logging.getLogger('multipart.multipart').setLevel(logging.ERROR)
Base.metadata.create_all(bind=get_engine())

app = FastAPI(title='m-peaks-mfi api', description='Mountain peaks API for MFI', version=ctx.VERSION, root_path="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
