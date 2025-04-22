# import random
# from datetime import datetime, timedelta
# from faker import Faker
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base, Department, Staff, Patient, PatientStaff, Vital, Credential

# # Initialize Faker and DB connection
# fake = Faker()
# engine = create_engine('sqlite:///patient_vitals.db')
# Session = sessionmaker(bind=engine)
# db = Session()

# # Create tables if they don't exist
# Base.metadata.create_all(engine)

# def create_departments():
#     departments = [
#         Department(name="ICU"),
#         Department(name="HDU"),
#         Department(name="Cardiology"),
#         Department(name="Pediatrics")
#     ]
#     db.add_all(departments)
#     db.commit()
#     return departments

# def create_staff(departments):
#     staff = []
#     roles = ["doctor", "nurse", "head_nurse"]
#     for _ in range(20):
#         staff.append(Staff(
#             name=fake.name(),
#             department_id=random.choice(departments).id,
#             role=random.choice(roles)
#         ))
#     db.add_all(staff)
#     db.commit()
#     return staff

# def create_credentials(staff_members):
#     credentials = []
#     for staff in staff_members:
#         raw_password = fake.password(length=5) # Raw password (to be deleted after testing)
#         credentials.append(Credential(
#             staff_id=staff.id,
#             password_hash=generate_password_hash(raw_password),  # Hashed random password
#             password_plaintext=raw_password # Temporarily store raw passwrod
#         ))
#         # print for testing
#         print(f"Staff {staff.id}: {raw_password}")
#     db.add_all(credentials)
#     db.commit()

# def create_patients(departments, staff):
#     patients = []
#     for _ in range(30):
#         admission_date = fake.date_time_between(start_date="-1y", end_date="now")
#         discharge_date = random.choice([None, fake.date_time_between(start_date=admission_date, end_date="now")])
        
#         patient = Patient(
#             name=fake.name(),
#             admission_date=admission_date,
#             discharge_date=discharge_date,
#             department_id=random.choice(departments).id
#         )
#         patients.append(patient)
#         db.add(patient)
    
#     db.commit()
    
#     # Assign staff to patients
#     for patient in patients:
#         for _ in range(random.randint(1, 3)):  # 1-3 staff per patient
#             db.add(PatientStaff(
#                 patient_id=patient.id,
#                 staff_id=random.choice(staff).id,
#                 role=random.choice(["primary", "secondary", "backup"])
#             ))
#     db.commit()
#     return patients

# def create_vitals(patients):
#     vitals = []
#     for patient in patients:
#         # Generate 1-5 vitals records per patient
#         for _ in range(random.randint(1, 5)):
#             timestamp = fake.date_time_between(
#                 start_date=patient.admission_date,
#                 end_date=patient.discharge_date or datetime.now()
#             )
#             vitals.append(Vital(
#                 patient_id=patient.id,
#                 systolic=random.randint(90, 180),
#                 diastolic=random.randint(60, 120),
#                 pulse_rate=random.randint(50, 100),
#                 blood_sugar=round(random.uniform(70, 200), 1),
#                 oxygen_volume=random.randint(90, 100),
#                 timestamp=timestamp
#             ))
#     db.add_all(vitals)
#     db.commit()
#     return vitals

# # if __name__ == "__main__":
# #     print("Generating mock data...")
# #     departments = create_departments()
# #     staff = create_staff(departments)
# #     patients = create_patients(departments, staff)
# #     vitals = create_vitals(patients)
# #     print(f"Created: {len(departments)} departments, {len(staff)} staff, {len(patients)} patients, {len(vitals)} vitals records")
