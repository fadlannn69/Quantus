from fastapi import FastAPI
from apk.api.v1.user import UserEndpoint
from apk.api.v1.content import ContentEndpoint
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from apk.database.session import engine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserEndpoint , prefix = '/user' , tags=['User'])
app.include_router(ContentEndpoint , prefix = '/content' , tags=['Content'])