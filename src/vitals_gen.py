from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Threshold, Alert, Vital
from faker import Faker
from models import Patient
from datetime import datetime
import time
import random

## fetch patients from the db
## after create a new vitals records after every 1 second
## these vitals will be pushed into the db

engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

def create_vitals(patients):
    vitals = []
    for patient in random.sample(patients, k=random.randint(1, len(patients))):
        timestamp = datetime.now()
        vital = Vital(
            patient_id=patient.id,
            systolic=random.randint(90, 180),
            diastolic=random.randint(60, 120),
            pulse_rate=random.randint(50, 100),
            blood_sugar=round(random.uniform(70, 200), 1),
            oxygen_volume=random.randint(90, 100),
            timestamp=timestamp
        )
        vitals.append(vital)
    
    db.add_all(vitals)
    db.commit()
    
def run_vitals_generation(patients):
    # patients = db.query(Patient).all()
    if not patients:
        print("No patients found.")
        return
    
    print("Starting continuous vitals generation...")
    try:
        while True:
            create_vitals(patients)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped vitals generation.")
                
