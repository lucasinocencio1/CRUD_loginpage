from fastapi import FastAPI
from database import engine
import models
from router import router

models.Base.metadata.create_all(bind=engine) #create the tables in the database

app = FastAPI()

app.include_router(router)


from auth import auth_router
app.include_router(auth_router)
