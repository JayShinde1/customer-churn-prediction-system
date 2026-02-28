from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    customerID = Column(String, primary_key=True, index=True)

    gender = Column(String(10), nullable=False)
    SeniorCitizen = Column(Integer)
    Partner = Column(Integer)
    Dependents = Column(Integer)
    tenure = Column(Integer, nullable=False)

    PhoneService = Column(Integer)
    MultipleLines = Column(Integer)
    InternetService = Column(String)
    OnlineSecurity = Column(Integer)
    OnlineBackup = Column(Integer)
    DeviceProtection = Column(Integer)
    TechSupport = Column(Integer)
    StreamingTV = Column(Integer)
    StreamingMovies = Column(Integer)

    Contract = Column(String)
    PaperlessBilling = Column(Integer)
    PaymentMethod = Column(String)

    MonthlyCharges = Column(Float, nullable=False)
    TotalCharges = Column(Float)
    


class ChurnPrediction(Base):
    __tablename__ = "churn_predictions"

    id = Column(Integer, primary_key = True, index = True)

    customer_id = Column(String, ForeignKey("customers.customerID"), nullable = False)
    churn_probability = Column(Float, nullable = False)
    predicted_churn = Column(Integer, nullable = False)

    created_at = Column(DateTime(timezone = True), server_default=func.now(), nullable = False)
    