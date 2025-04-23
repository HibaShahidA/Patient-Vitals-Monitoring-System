from models import Patient
from db_connect import SessionLocal

db = SessionLocal()

def fetch_patient_details(patient_id):
    # Fetch patient record
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if patient:
        name = patient.name
        dob = patient.date_of_birth
        gender = patient.gender
        prim_phone = patient.primary_contact
        sec_phone = patient.secondary_contact
        admission_date = patient.admission_date
        discharge_date = patient.discharge_date

        # Department
        dept = patient.department.name if patient.department else None

        # Emergency Contact
        if patient.emergency_contacts:
            emerg_contact_name = patient.emergency_contacts[0].name
            emerg_contact_relation = patient.emergency_contacts[0].relation
            emerg_contact_contact = patient.emergency_contacts[0].contact
        else:
            emerg_contact_name = emerg_contact_relation = emerg_contact_contact = None

        # History
        allergies = patient.history.allergies if patient.history else None
        prev_conditions = patient.history.prev_conditions if patient.history else None

        # Medications (getting a list of medicine names)
        meds = [med.medicine.name for med in patient.medications]

        # Assigned staff
        prim_doc = next((s.staff.name for s in patient.staff_assignments if s.role == "primary"), None)
        sec_doc = next((s.staff.name for s in patient.staff_assignments if s.role == "secondary"), None)
        head_nurse = next((s.staff.name for s in patient.staff_assignments if s.role == "backup"), None)

        for assignment in patient.staff_assignments:
            role = assignment.role
            staff_member = assignment.staff
            if role == "primary_doctor":
                prim_doc = staff_member.name
            elif role == "secondary_doctor":
                sec_doc = staff_member.name
            elif role == "head_nurse":
                head_nurse = staff_member.name
    else:
        print("Patient not found.")
        
    return {
        "name": name,
        "dob": dob,
        "gender": gender,
        "primary_contact": prim_phone,
        "secondary_contact": sec_phone,
        "admission_date": admission_date,
        "discharge_date": discharge_date,
        "department": dept,
        "emergency_contact": {
            "name": emerg_contact_name,
            "relation": emerg_contact_relation,
            "contact": emerg_contact_contact
        },
        "allergies": allergies,
        "previous_conditions": prev_conditions,
        "medications": meds,
        "staff": {
            "primary_doctor": prim_doc,
            "secondary_doctor": sec_doc,
            "head_nurse": head_nurse
        }
    }

    