from fastapi import FastAPI, Form
import joblib  # or pickle if you used that for serialization
import pickle

# Load your pre-trained model and scaler
with open(r"C:\Users\g_bhu\OneDrive - VeBuIn\Modify webapi\scalerr.pkl", "rb") as f:
    scaler = pickle.load(f)

# Initialize FastAPI app
app = FastAPI()

# Load your pre-trained model
with open(r"C:\Users\g_bhu\OneDrive - VeBuIn\Modify webapi\pre_logg.pkl", "rb") as f:
    model = pickle.load(f)

# Define your prediction endpoint
@app.post("/predict/")
async def predict_quality(
    fixed_acidity: float = Form(...), 
    volatile_acidity: float = Form(...), 
    citric_acid: float = Form(...), 
    chlorides: float = Form(...),
    total_sulfur_dioxide: float = Form(...),
    density: float = Form(...),
    sulphates: float = Form(...),
    alcohol: float = Form(...)): 
                         
    # Prepare input data
    input_data = [[fixed_acidity, volatile_acidity, citric_acid, chlorides, total_sulfur_dioxide, density, sulphates, alcohol]]
    
    # Scale the input data
    scaled_data = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(scaled_data)
    pred = model.predict_proba(scaled_data)
    print(pred)
    
    # Return prediction along with input data
    return {"prediction": prediction[0]}
