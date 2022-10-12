from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from . import mymodels
from .dbase import  engine
from .routers import mypost, myusers, auth_login, mylikes
from .config import settings

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mypost.router)
app.include_router(myusers.router)
app.include_router(auth_login.router)
app.include_router(mylikes.router)


@app.get('/')
def root():
    return {"message":"je ferai de grandes choses!"} 



