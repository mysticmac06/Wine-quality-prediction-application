from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    fixed_acidity = Column(Float)  # Add this line
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    chlorides = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    quality = Column(Float)  
    model_used = Column(String)
    best_probability = Column(Float)

    def __repr__(self):
        return f'<User {self.id}>'