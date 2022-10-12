from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import time



while  True:
    try:
       conn = psycopg2.connect(host=f'{settings.DATABASE_HOSTNAME}',database=f'{settings.DATABASE_NAME}',user=f'{settings.DATABASE_USERNAME}',password=f'{settings.DATABASE_PASSWORD}', cursor_factory=RealDictCursor)
   
       cursor = conn.cursor()  
       print("Database was connected succesfully !")
       break
        
          
    except Exception as error:
        print("Oops try again !")
        print("Error:", error)
        time.sleep(2)
        
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

