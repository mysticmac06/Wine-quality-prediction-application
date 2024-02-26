from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from predict import predict_quality 

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/add")
async def add(request: Request, name: str = Form(...), fixed_acidity: float = Form(...), volatile_acidity: float = Form(...), citric_acid: float = Form(...), chlorides: float = Form(...), total_sulfur_dioxide: float = Form(...), density: float = Form(...), sulphates: float = Form(...), alcohol: float = Form(...), db: Session = Depends(get_db)):
    # Call predict_quality coroutine to get prediction
    prediction = await predict_quality(fixed_acidity, volatile_acidity, citric_acid, chlorides, total_sulfur_dioxide, density, sulphates, alcohol)
    
    # Extract the prediction value
    quality = prediction['prediction']
    
    # Create a new User instance with the predicted quality
    user = models.User(name=name, fixed_acidity=fixed_acidity, volatile_acidity=volatile_acidity, citric_acid=citric_acid, chlorides=chlorides, total_sulfur_dioxide=total_sulfur_dioxide, density=density, sulphates=sulphates, alcohol=alcohol, quality=quality)
    
    # Add the user to the database
    db.add(user)
    db.commit()
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})

@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), fixed_acidity: float = Form(...), volatile_acidity: float = Form(...), citric_acid: float = Form(...), chlorides: float = Form(...), total_sulfur_dioxide: float = Form(...), density: float = Form(...), sulphates: float = Form(...), alcohol: float = Form(...), db: Session = Depends(get_db)):
    # Call predict_quality function to get prediction
    prediction = await predict_quality(fixed_acidity, volatile_acidity, citric_acid, chlorides, total_sulfur_dioxide, density, sulphates, alcohol)
    
    # Retrieve the user from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Update user's information including the predicted quality
    user.name = name
    user.fixed_acidity = fixed_acidity
    user.volatile_acidity = volatile_acidity
    user.citric_acid = citric_acid
    user.chlorides = chlorides
    user.total_sulfur_dioxide = total_sulfur_dioxide
    user.density = density
    user.sulphates = sulphates
    
    
    # Convert prediction to float if it's a dictionary
    if isinstance(prediction, dict):
        quality = prediction.get('prediction', 0.0)
    else:
        quality= float(prediction)
    
    # Assign prediction to user's quality
    user.quality = quality
    
    # Commit the changes to the database
    db.commit()
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
