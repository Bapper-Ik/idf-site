from fastapi import APIRouter, Depends, Form, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Annotated

from app import database, models, schemas
# from app.utils.serializers import
from app.utils import oauth2

from pathlib import Path
from datetime import date, time, datetime

from pydantic import FutureDate

router = APIRouter(
    prefix="/admin/dashboard",
    tags=['Admin']
)


@router.get('/')
async def admin_dashboard(admin: schemas.Admin = Depends(oauth2.get_current_user)):
    return {"msg": "this is admin dashboard page"}


@router.post('/add_category', response_model=schemas.Category)
async def add_category(category_name: Annotated[str, Form()], db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    
    try:        
        existed_category = db.query(models.Category).filter(models.Category.name == category_name).first()

        if existed_category:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"{category_name.capitalize()} already exist!")
        
        new_category = models.Category(name=category_name.lower())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        
        return new_category
    except Exception as e:
        raise e
    

@router.put('/taalim/update_category/{category_id}')
async def update_cateegory(category_id: int, category_name: Annotated[str, Form()], db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    
    try:
        category_Query = db.query(models.Category).filter(models.Category.id == category_id)
    
        current_category = category_Query.first()
    
        if not current_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} was not found!")
        
        category_Query.update(values = {"name": category_name.lower()}, synchronize_session=False)
        db.commit()
        db.refresh(current_category)
        
        return current_category
    
    
    except Exception as e:
        raise e



@router.delete('/taalim/delete_category/{category_id}')
async def delete_category(category_id: int, db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    try:
        current_category = db.query(models.Category).filter(models.Category.id == category_id).first()
        
        if not current_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {category_id} was not found!")
        
        db.delete(current_category)
        db.commit()
        
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Category deleted successfully!")
    except Exception as e:
        raise e


@router.post('/ta_alim/add_ta_alim', response_model=schemas.BaseTaalim)
async def add_ta_alim(file: UploadFile, ta_alim_name: Annotated[str, Form()], category_name: Annotated[str, Form()], db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):

    try:
        category = db.query(models.Category).filter(models.Category.name == category_name.lower()).first()
        
        query_taalim = db.query(models.TaAlim).filter(models.TaAlim.name == ta_alim_name.lower())        
        existed_taalim = query_taalim.first()
        
        if existed_taalim:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Ta'alim already exist!")

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{category_name.capitalize()} was not found!")
        
        
        UPLOAD_DIR = Path() / 'uploads' / 'ta_alims'
        save_to = UPLOAD_DIR / file.filename
        file_data = await file.read()
        
        with open(save_to, 'wb') as f:
            f.write(file_data)
        
        file_path = str(save_to)
        new_taalim = models.TaAlim(name=ta_alim_name.lower(), url=file_path.lower(), ta_alim_category_id=category.id)               
        db.add(new_taalim)
        db.commit()
        db.refresh(new_taalim)

        return new_taalim

    except Exception as e:
        raise e
    


@router.put('/taalim/update_taalim/{ta_alim_id}')
async def update_ta_alim(ta_alim_id: int, file: UploadFile, ta_alim_name: Annotated[str, Form()], category_name: Annotated[str, Form()], db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):

    try:
        ta_alim_query = db.query(models.TaAlim).filter(models.TaAlim.id == ta_alim_id)
        
        current_ta_alim = ta_alim_query.first()
        
        category = db.query(models.Category).filter(models.Category.name == category_name.lower()).first()
        
        if not current_ta_alim:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ta'Alim with id {ta_alim_id} was not found!")
        
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{category_name.capitalize()} was not found!")
        
        
        UPLOAD_DIR = Path() / 'uploads' / 'ta_alims'
        save_to = UPLOAD_DIR / file.filename
        file_data = await file.read()
        
        with open(save_to, 'wb') as f:
            f.write(file_data)
        
        file_path = str(save_to)
        ta_alim_query.update(values={"name":ta_alim_name.lower(), "url": file_path.lower(), "ta_alim_category_id": category.id}, synchronize_session=False)
        db.commit()
        db.refresh(current_ta_alim)
        
        return current_ta_alim
    
    except Exception as e:
        raise e



@router.delete('/taalim/delete_ta_alim/{taalim_id}')
async def delete_category(taalim_id: int, db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    try:
        current_taalim = db.query(models.TaAlim).filter(models.TaAlim.id == taalim_id).first()
        
        if not current_taalim:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ta'alim with id {taalim_id} was not found!")
        
        db.delete(current_taalim)
        db.commit()
        
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ta'alim deleted successfully!")
    except Exception as e:
        raise e


@router.post('/add_event')
async def add_event(event_name: Annotated[str, Form()], start_date: Annotated[date, Form()], end_date: Annotated[FutureDate, Form()], venue: Annotated[str, Form()], time: Annotated[time, Form()] = time(00,00,00), db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    try:
        existed_event = db.query(models.Event).filter(models.Event.name == event_name).first()
        
        if existed_event:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Event already exist")
        
        new_event = models.Event(name=event_name.lower(), start_date=start_date, end_date=end_date, venue=venue.lower(), time=time)
        
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        
        return new_event
    except Exception as e:
        raise e


@router.put('/event/update_event/{event_id}')
async def update_ta_alim(event_id: int, event_name: Annotated[str, Form()], start_date: Annotated[date, Form()], end_date: Annotated[date, Form()], venue: Annotated[str, Form()], isCompleted: Annotated[bool, Form()],time: Annotated[time, Form()] = time(00,00,00), db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    
    try:
        event_query = db.query(models.Event).filter(models.Event.id == event_id)
        
        current_event = event_query.first()
        
        if not current_event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} was not found!")
        
        event_query.update(values = {"name": event_name.lower(), "start_date": start_date, "end_date": end_date, "venue": venue.lower(), "time": time, "isCompleted": isCompleted}, synchronize_session=False)
        
        db.commit()
        db.refresh(current_event)
        
        return current_event
    
    except Exception as e:
        raise e


@router.delete('/event/delete_event/{event_id}')
async def delete_category(event_id: int, db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    try:
        current_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        
        if not current_event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {event_id} was not found!")
        
        db.delete(current_event)
        db.commit()
        
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Event deleted successfully!")
    except Exception as e:
        raise e


@router.post('/add_images')
async def add_image(file: UploadFile, caption: Annotated[str, Form()], db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):
    try:
        existed_image = db.query(models.Images).filter(models.Images.caption == caption).first()
        
        if existed_image:
            print(existed_image.id)
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Image already exist!")
        
        UPLOAD_DIR = Path() / 'uploads' / 'images'
        file_data = await file.read()
        save_to = UPLOAD_DIR / file.filename
        path = str(save_to)
        
        with open(save_to, 'wb') as f:
            f.write(file_data)        
        
        new_image = models.Images(url=path, caption=caption)
        
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return new_image
    except Exception as e:
        raise e


@router.put('/gallery/update_image/{image_id}')
async def update_image(file: Annotated[UploadFile, File()], caption: Annotated[str, Form()], image_id: int, db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):

    try:    
        image_query = db.query(models.Images).filter(models.Images.id == image_id)

        current_image = image_query.first()

        if not current_image:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Image with id {image_id} was not found!")


        UPLOAD_DIR = Path() / 'uploads' / 'images'
        file_data = await file.read()
        save_to = UPLOAD_DIR / file.filename
        path = str(save_to)

        with open(save_to, 'wb') as f:
            f.write(file_data)   

        image_query.update(values = {"url": path, "caption": caption}, synchronize_session=False)
        db.commit()
        db.refresh(current_image)

        return current_image
    except Exception as e:
        raise e


@router.delete('/gallery/delete_image/{image_id}')
async def delete_image(image_id: int, db: Session = Depends(database.get_db), admin: schemas.Admin = Depends(oauth2.get_current_user)):  
    
    try:
        current_image = db.query(models.Images).filter(models.Images.id == image_id).first()

        if not current_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Image with id {image_id} was not found!")

        db.delete(current_image)
        db.commit()

        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Image deleted successfully!")
    except Exception as e:
        raise e






