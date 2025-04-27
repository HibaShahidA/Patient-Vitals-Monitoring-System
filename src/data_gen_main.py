from static_data_gen import create_static_data
from vitals_gen import run_vitals_generation
from anomaly_detection import run_anomaly_detection
from threshold_data import create_thresholds
from models import Staff, Credential, Patient, PatientStaff
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from static_data_gen import fake

from multiprocessing import Process

# def add_dummy_staff(session):
#     # Create dummy doctor
#     doctor = Staff(role="doctor", name="Dr. John Doe")
#     session.add(doctor)
#     session.commit()  # Commit to get the doctor ID

#     # Create the credential for the doctor
#     doctor_password = "doctor123"  # Custom password for doctor
#     hashed_password = generate_password_hash(doctor_password)
#     credential = Credential(staff_id=doctor.id, password_hash=hashed_password, password_plaintext=doctor_password)
#     session.add(credential)

#     # Create dummy non-doctor staff
#     non_doctor = Staff(role="non-doctor", name="Nurse Jane")
#     session.add(non_doctor)
#     session.commit()  # Commit to get the non-doctor ID

#     # Create the credential for the non-doctor
#     non_doctor_password = "nurse123"  # Custom password for non-doctor
#     hashed_password = generate_password_hash(non_doctor_password)
#     credential = Credential(staff_id=non_doctor.id, password_hash=hashed_password, password_plaintext=non_doctor_password)
#     session.add(credential)
    
#     patient = Patient(
#         name="Patient One",
#         admission_date=fake.date_this_year(),  # Dummy admission date, generated randomly
#         discharge_date=fake.date_this_year(),  # Dummy discharge date, generated randomly
#         department_id=4,  # Randomly choose a department
#         date_of_birth=fake.date_of_birth(minimum_age=0, maximum_age=90),  # Random date of birth between 0 and 90 years
#         gender="Female",  # Set the gender
#         primary_contact=fake.random_number(digits=11),  # Dummy contact number
#         secondary_contact=fake.random_number(digits=11),  # Dummy secondary contact number
#     )
#     session.add(patient)
#     session.commit()  # Commit to get the patient ID

#     # Associate patient 1 with the doctor (Doctor is assigned to this patient)
#     patient_staff = PatientStaff(patient_id=patient.id, staff_id=doctor.id, role="primary")  # Assign doctor as primary
#     session.add(patient_staff)

#     session.commit()  # Final commit
    
    
def create_database_session():
    engine = create_engine('sqlite:///patient_vitals.db')  # Replace with your DB path
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Create a database session
    session = create_database_session()
    
    # Add dummy staff, patient, and association
    # add_dummy_staff(session)
    
    # Base data
    patients = create_static_data()
    create_thresholds()
    
    # Vitals generation and Anomaly detection
    vitals_proc = Process(target=run_vitals_generation, args=(patients,))
    anomaly_proc = Process(target=run_anomaly_detection, args=(patients,))
    
    vitals_proc.start()
    anomaly_proc.start()
    
    try:
        vitals_proc.join()
        anomaly_proc.join()
    except KeyboardInterrupt:
        print("Keyboard Interrupt received. Terminating process...")
        vitals_proc.terminate()
        anomaly_proc.terminate()
