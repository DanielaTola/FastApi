from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="My first api", 
    description= "Esta es mi primer api con FastApi",
    version="0.0.1",
    openapi_tags=[{
            "name":"users", 
        "description":"users routes"
    }]
)

app.include_router(user)
