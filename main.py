from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

engine = create_engine("sqlite:///patients.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    diagnosis = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String, unique=True, nullable=True)

Base.metadata.create_all(bind=engine)

class PatientCreate(BaseModel):
    name: str
    phone: str
    diagnosis: str
    blood_type: str
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    diagnosis: str
    blood_type: str
    age: Optional[int] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Patient Records API")

@app.get("/")
def root():
    return {"message": "This is a patient records API"}

@app.get("/patients/", response_model=List[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    """Get all patients"""
    patients = db.query(Patient).all()
    for p in patients:
        if p.diagnosis:
            p.diagnosis = p.diagnosis[:3] + "*" * (len(p.diagnosis) - 3)
    return patients

@app.get("/patients/search/", response_model=List[PatientResponse])
def search_patients_by_phone(phone: str, db: Session = Depends(get_db)):
    """Search patients on phonenumber"""
    results = db.query(Patient).filter(Patient.phone == phone).all()
    if not results:
        raise HTTPException(status_code=404, detail="No patients found with this phone number")
    for p in results:
        if p.diagnosis:
            p.diagnosis = p.diagnosis[:3] + "*" * (len(p.diagnosis) - 3)
    
    return results

@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Search patient on ID"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient.diagnosis:
        patient.diagnosis = patient.diagnosis[:3] + "*" * (len(patient.diagnosis) - 3)
    return patient

@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Add a new patient"""
    if db.query(Patient).filter(Patient.phone == patient.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")
    if not patient.phone.isdigit() or len(patient.phone) != 10:
        raise HTTPException(status_code=400, detail="Phone number must be exactly 10 digits")
    
    if patient.email and db.query(Patient).filter(Patient.email == patient.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if patient.age is not None and patient.age < 0:
        raise HTTPException(status_code=400, detail="Age must be positive")
    
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    if db_patient.diagnosis:
        db_patient.diagnosis = db_patient.diagnosis[:3] + "*" * (len(db_patient.diagnosis) - 3)

    return db_patient

@app.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):
    """Update patiëntgegevens"""
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if patient.email and patient.email != db_patient.email:
        if db.query(Patient).filter(Patient.email == patient.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    if patient.age is not None and patient.age < 0:
        raise HTTPException(status_code=400, detail="Age must be positive")
    
    for field, value in patient.dict().items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    if db_patient.diagnosis:
        db_patient.diagnosis = db_patient.diagnosis[:3] + "*" * (len(db_patient.diagnosis) - 3)
    
    return db_patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Verwijder een patiënt"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}
