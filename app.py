from database import db_dependency
from fastapi import FastAPI, Path
from starlette import status
from models import ChurnPrediction, Customer
import pandas as pd
import numpy as np
import joblib
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
from sqlalchemy import func

app = FastAPI()

pipeline = joblib.load("./model/model.pkl")
threshold = 0.45

class InputData(BaseModel):
    gender: str = Field(...)
    SeniorCitizen : int 
    Partner : int 
    Dependents: int
    tenure: int = Field(...)

    PhoneService: int
    MultipleLines: int
    InternetService: str
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int

    Contract: str
    PaperlessBilling: int
    PaymentMethod: str

    MonthlyCharges: float = Field(...)
    TotalCharges: float


@app.post('/predict/{customer_id}', status_code = status.HTTP_201_CREATED)
def predict_churn(customer_id: str, db: db_dependency, user_input: InputData):
    customer = db.query(Customer).filter(Customer.customerID == customer_id).first()

    if not customer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Customer ID not found.")

    customer_dict = {column.name: getattr(customer, column.name) 
                     for column in Customer.__table__.columns}

    df = pd.DataFrame([customer_dict])

    prob = pipeline.predict_proba(df)[0][1]
    prediction = int(prob >= threshold)

    prediction_row = ChurnPrediction(
        customer_id = customer_id,
        churn_probability = float(prob),
        predicted_churn = prediction
    )

    db.add(prediction_row)
    db.commit()

    return {
            "customer_id": customer_id,
            "probability": float(prob),
            "prediction": prediction
        }


@app.get("/top-risk")
def get_top_risk( db: db_dependency, n: int = 10):

    subquery = (
        db.query(
            ChurnPrediction.customer_id,
            func.max(ChurnPrediction.created_at).label("latest_time")
        )
        .group_by(ChurnPrediction.customer_id)
        .subquery()
    )

    latest_predictions = (
        db.query(ChurnPrediction)
        .join(
            subquery,
            (ChurnPrediction.customer_id == subquery.c.customer_id) &
            (ChurnPrediction.created_at == subquery.c.latest_time)
        )
        .order_by(ChurnPrediction.churn_probability.desc())
        .limit(n)
        .all()
    )

    return latest_predictions