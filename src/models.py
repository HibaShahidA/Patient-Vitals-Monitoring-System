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
    department = relationship("Department", back_populates="staff")
    patient_assignments = relationship("PatientStaff", back_populates="staff")

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
    admission_date = Column(DateTime)
    discharge_date = Column(DateTime, nullable=True)
    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department", back_populates="patients")
    vitals = relationship("Vital", back_populates="patient")
    staff_assignments = relationship("PatientStaff", back_populates="patient")
    alerts = relationship("Alert", back_populates="patient")

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
