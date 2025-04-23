from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Staff, PatientStaff

# Setup database connection
engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

def authenticate_staff(staff_id, password):
    """Check if staff ID and password match a user in the database."""
    staff = db.query(Staff).filter_by(id=staff_id, password=password).first()
    db.close()

    if staff:
        return {"staff_id": staff.id, "role": staff.role}
    return None

def is_authorized_for_patient(staff_id, patient_id):
    """Check if the staff member is authorized to access the patient's data."""
    access = db.query(PatientStaff).filter_by(staff_id=staff_id, patient_id=patient_id).first()
    db.close()

    return access is not None
