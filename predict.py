from fastapi import FastAPI, Form, HTTPException
import pickle
import numpy as np
app = FastAPI()

# Load your pre-trained model and scaler
with open(r"scalerr(1).pkl", "rb") as f:
    scaler = pickle.load(f)

# Load your pre-trained models
with open(r"pre_logg(1).pkl", "rb") as f:
    model = pickle.load(f)

with open(r"pre_svc(1).pkl", "rb") as f:
    svc_model = pickle.load(f)

with open(r"pre_knn(1).pkl", "rb") as f:
    knn = pickle.load(f)

with open(r"pre_dt.pkl", "rb") as f:
    tree = pickle.load(f)

with open(r"pre_RF.pkl", "rb") as f:
    rf = pickle.load(f)

with open(r"pre_GB.pkl", "rb") as f:
    gb_classifier = pickle.load(f)

with open(r"pre_XGB.pkl", "rb") as f:
    xgb_ = pickle.load(f)

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
    alcohol: float = Form(...),
    selected_model: str = Form(...)):

    # Prepare input data
    input_data = [[fixed_acidity, volatile_acidity, citric_acid, chlorides, total_sulfur_dioxide, density, sulphates, alcohol]]

    # Scale the input data
    scaled_data = scaler.transform(input_data)

    # Make prediction using the selected model
    if selected_model == "Logistic":
        prediction = model.predict(scaled_data)
        pred_proba = model.predict_proba(scaled_data)
        
        
    elif selected_model == "SVC":
        prediction = svc_model.predict(scaled_data)
        pred_proba = svc_model.predict_proba(scaled_data)
        

    elif selected_model == "KNN":
        prediction = knn.predict(scaled_data)
        pred_proba = knn.predict_proba(scaled_data)
        

    elif selected_model == "Decision tree":
        prediction = tree.predict(scaled_data)
        pred_proba = tree.predict_proba(scaled_data)
        

    elif selected_model == "Random Forest":
        prediction = rf.predict(scaled_data)
        pred_proba = rf.predict_proba(scaled_data)
        

    elif selected_model == "Gradient Boost":
        prediction = gb_classifier.predict(scaled_data)
        pred_proba = gb_classifier.predict_proba(scaled_data)
        

    elif selected_model == "XGBoost":
        prediction = xgb_.predict(scaled_data)
        pred_proba = xgb_.predict_proba(scaled_data)
        

    else:
        pass

    

    best_class_index = np.argmax(pred_proba)
    best_probability = pred_proba[0][best_class_index]
    best_probability = "{:.2f}".format(best_probability * 100)

    return {"prediction": prediction[0], "best_probability": best_probability}



    
