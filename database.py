from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
 
DB_URL = 'postgresql://bhu:1234@localhost:5432/wine'
 
engine = create_engine(DB_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





# 'postgresql://postgres:1234@5432/Fastapidb'