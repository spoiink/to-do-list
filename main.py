from fastapi import FastAPI



from app.dataBase import Base, engine
from app import models
from app.api.v1.auth import router as users_router
from app.api.v1.profile import router as profile_router

app = FastAPI()


app.include_router(users_router, prefix='/api/v1', tags=['auth'])
app.include_router(profile_router, prefix='/api/v1', tags=['profile'])

Base.metadata.create_all(bind=engine)

