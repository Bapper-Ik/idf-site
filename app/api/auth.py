from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app import models
from app.utils import utils, oauth2
from app.utils.serializers import user_serializer

from app.utils.oauth2 import oauth2_scheme

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)



def first_migration(username: str, password: str):
    hashed_password = utils.hashing(password)
    first_migration_data = {
        "username": username,
        "password": hashed_password,
        "role": 1
    }
    
    try:
        admin = models.Users(**first_migration_data)
        return admin
    except Exception as e:
        raise e


@router.post('/login')
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existed_admin = db.query(models.Users).filter(models.Users.role == 1).first()
    try:
        if not existed_admin:
            admin = first_migration(user_cred.username, user_cred.password)
            db.add(admin)
            db.commit()

        current_admin = db.query(models.Users).filter(models.Users.username == user_cred.username).first()

        if not current_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
            
        if not utils.verify_password(user_cred.password, current_admin.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")


        access_token = oauth2.create_access_token(data={"user_info": user_serializer(current_admin)})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise e