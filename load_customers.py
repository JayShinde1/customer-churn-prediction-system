from sqlalchemy.orm import Session
from database import Session_local
from models import Customer
import pandas as pd

df = pd.read_csv("dataset/cleaned_churn.csv")  

db: Session = Session_local()

try:
    for row in df.itertuples(index=False):
        customer = Customer(
            customerID=row.customerID,
            gender=row.gender,
            SeniorCitizen=row.SeniorCitizen,
            Partner=row.Partner,
            Dependents=row.Dependents,
            tenure=row.tenure,
            PhoneService=row.PhoneService,
            MultipleLines=row.MultipleLines,
            InternetService=row.InternetService,
            OnlineSecurity=row.OnlineSecurity,
            OnlineBackup=row.OnlineBackup,
            DeviceProtection=row.DeviceProtection,
            TechSupport=row.TechSupport,
            StreamingTV=row.StreamingTV,
            StreamingMovies=row.StreamingMovies,
            Contract=row.Contract,
            PaperlessBilling=row.PaperlessBilling,
            PaymentMethod=row.PaymentMethod,
            MonthlyCharges=row.MonthlyCharges,
            TotalCharges=row.TotalCharges
        )

        db.add(customer)

    db.commit()
    print("Customers inserted successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()