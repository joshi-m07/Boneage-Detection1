from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class Patient(Base):
    """Patient table for storing patient information and images"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True, nullable=False)
    image_path = Column(String, nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient(patient_id='{self.patient_id}')>"


class Prediction(Base):
    """Prediction table for storing bone age predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # Male model predictions
    male_age = Column(Float, nullable=False)
    male_uncertainty = Column(Float, nullable=False)
    male_gradcam_path = Column(String, nullable=True)
    
    # Female model predictions
    female_age = Column(Float, nullable=False)
    female_uncertainty = Column(Float, nullable=False)
    female_gradcam_path = Column(String, nullable=True)
    
    # MLflow tracking
    mlflow_run_id = Column(String, nullable=True)
    
    # Metadata
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to patient
    patient = relationship("Patient", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(male_age={self.male_age}, female_age={self.female_age})>"
