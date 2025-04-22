from db_connect import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey("department.id"))
    role = Column(String)  # "doctor", "nurse"
    contact = Column(Integer)
    
    department = relationship("Department", back_populates="staff")
    patient_assignments = relationship("PatientStaff", back_populates="staff")
    credential = relationship("Credential", back_populates="staff", uselist=False)

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    staff = relationship("Staff", back_populates="department")
    patients = relationship("Patient", back_populates="department")

class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    primary_contact = Column(Integer)
    secondary_contact = Column(Integer)
    admission_date = Column(DateTime)
    discharge_date = Column(DateTime, nullable=True)
    department_id = Column(Integer, ForeignKey("department.id"))
    
    department = relationship("Department", back_populates="patients")
    vitals = relationship("Vital", back_populates="patient")
    staff_assignments = relationship("PatientStaff", back_populates="patient")
    alerts = relationship("Alert", back_populates="patient")
    
    emergency_contacts = relationship("Emergency_Contact", back_populates="patient")
    history = relationship("Patient_History", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")

class Emergency_Contact(Base):
    __tablename__ = "emergency_contact"
    patient_id = Column(Integer, ForeignKey("patient.id"), primary_key=True)
    name = Column(String)
    relation = Column(String) # spouse, parent, child (son or daughter)
    contact = Column(Integer)
    
    patient = relationship("Patient", back_populates="emergency_contacts")

class Patient_History(Base):
    __tablename__ = "patient_history"
    patient_id = Column(Integer, ForeignKey("patient.id"), primary_key=True)
    allergies = Column(String)
    prev_conditions = Column(String)
    # current_medication to be accessed through the table medication
    patient = relationship("Patient", back_populates="history", uselist=False)
    
class Medication(Base):
    __tablename__ = "medication"
    med_id = Column(Integer, ForeignKey("medicine.id"), primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), primary_key=True)
    dosage_times = Column(String)
    
    medicine = relationship("Medicine", back_populates="medications")
    patient = relationship("Patient", back_populates="medications")
    
class Medicine(Base):
    __tablename__ = "medicine"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = Column(String)
    
    medications = relationship("Medication", back_populates="medicine")
    
class Vital(Base):
    __tablename__ = "vital"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    systolic = Column(Integer)
    diastolic = Column(Integer)  # Fixed typo
    pulse_rate = Column(Integer)
    blood_sugar = Column(Float)
    oxygen_volume = Column(Float)
    timestamp = Column(DateTime)
    
    patient = relationship("Patient", back_populates="vitals")

class Alert(Base):
    __tablename__ = "alert"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    message = Column(String)
    severity = Column(String)  # "low", "medium", "high"
    timestamp = Column(DateTime)
    
    patient = relationship("Patient", back_populates="alerts")

class PatientStaff(Base):
    __tablename__ = "patient_staff"
    patient_id = Column(Integer, ForeignKey("patient.id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    role = Column(String)  # "primary_doctor", "secondary_nurse"
    
    patient = relationship("Patient", back_populates="staff_assignments")
    staff = relationship("Staff", back_populates="patient_assignments")

class Credential(Base):
    __tablename__ = "credentials"
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    password_hash = Column(String(128), nullable=False)  # Stores hashed passwords
    # TODO: TEMPORARY FIELD (to be removed after testing)
    password_plaintext = Column(String(50), nullable=True)  # Stores raw password
    
    staff = relationship("Staff", back_populates="credential")
    
# Threshold for reference ---- to remain constant
class Threshold(Base):
    __tablename__ = "threshold"
    id = Column(Integer, primary_key=True)
    
    # Demographic filters
    age_lower = Column(Integer, nullable=False)
    age_upper = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # e.g., "male", "female", "other"
    
    # Lower bounds for vitals
    systolic_lower = Column(Integer, nullable=False)
    diastolic_lower = Column(Integer, nullable=False)
    blood_sugar_lower = Column(Float, nullable=False)
    pulse_rate_lower = Column(Integer, nullable=False)
    oxygen_levels_lower = Column(Float, nullable=False)
    
    # Upper bounds for vitals
    systolic_upper = Column(Integer, nullable=False)
    diastolic_upper = Column(Integer, nullable=False)
    blood_sugar_upper = Column(Float, nullable=False)
    pulse_rate_upper = Column(Integer, nullable=False)
    oxygen_levels_upper = Column(Float, nullable=False)
