from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, database, schemas


router = APIRouter(
    tags=['Client']
)


@router.get('/taalim/categories/all_categories', response_model=list[schemas.CategoryResponseModel])
async def get_all_categories(db: Session = Depends(database.get_db)):

    try:
        categories = db.query(models.Category).all()
        
        if not categories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No category was found!")
        
        return categories
    
    except Exception as e:
        raise e


@router.get('/taalim/all_ta_alims', response_model=list[schemas.TaAlimResponseModel])
async def get_all_ta_alims(db: Session = Depends(database.get_db)):
    try:
        taalims = db.query(models.TaAlim).all()
        
        if not taalims:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ta'alim was found!")
        
        return taalims
    
    except Exception as e:
        raise e


@router.get('/taalim/{category_id}/all_taalims', response_model=list[schemas.TaAlimResponseModel])
async def get_all_taalims_by_category(category_id: int, db: Session = Depends(database.get_db)):
    
    try:    
        ta_alims = db.query(models.TaAlim).filter(models.TaAlim.ta_alim_category_id == category_id).all()
        
        if not ta_alims:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ta'alim was found!")
        
        return ta_alims
    
    except Exception as e:
        raise e


@router.get('/taalim/{category_id}/{ta_alim_id}', response_model=schemas.TaAlimResponseModel)
async def get_ta_alim_category_id(category_id: int, ta_alim_id: int, db: Session = Depends(database.get_db)):
    
    try:
        ta_alim = db.query(models.TaAlim).filter(models.TaAlim.ta_alim_category_id == category_id, models.TaAlim.id == ta_alim_id).first()

        if not ta_alim:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ta'alim with id {ta_alim_id} was not found!")
        
        return ta_alim
    
    except Exception as e:
        raise e
    
    
@router.get('/gallery/all_images', response_model=list[schemas.BaseImgae])
async def get_all_images(db: Session = Depends(database.get_db)):
    try:
        images = db.query(models.Images).all()
        
        if not images:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image was found!")
        
        return images
    except Exception as e:
        raise e


@router.get('/events/all_events')
async def get_all_images(db: Session = Depends(database.get_db)):
    try:
        events = db.query(models.Event).all()
        
        if not events:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No event was found!")
        
        return events
    except Exception as e:
        raise e
