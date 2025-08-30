
from app.api import routers

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Starting')
    yield
    print('Stopping')


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    print(f"Accessing {request.url.path}")
    response = await call_next(request)
    print(f"Finished {request.url.path}")
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[],          # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # ["GET", "POST"] if you want to restrict
    allow_headers=["*"],            # ["Authorization", "Content-Type"] if restricted)
)


app.include_router(router=routers, prefix='/api/v1')
