from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = f'postgresql://idf_site_user:HfB8GF7xwcJ4cWLwhbpYG8X2hevY3CMa@dpg-cq4h6emehbks73bbj42g-a.oregon-postgres.render.com/idf_site'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

