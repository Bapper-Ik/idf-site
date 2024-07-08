from fastapi import FastAPI
from app import models
from app.database import engine

from app.api import client, admin, auth
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)



@app.get('/')
async def root():
    return {"status": "Server's up and running..."}


app.include_router(client.router)
app.include_router(admin.router)
app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port=8000)
    
    