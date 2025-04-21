import sqlite3

DB_PATH = 'src/database.db'

def authenticate_staff(staff_id, password):
    """Check if staff ID and password match a user in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role FROM staff WHERE id = ? AND password = ?", (staff_id, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"staff_id": result[0], "role": result[1]}
    return None

def is_authorized_for_patient(staff_id, patient_id):
    """Check if the staff member is authorized to access the patient's data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patient_access WHERE staff_id = ? AND patient_id = ?", (staff_id, patient_id))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None
