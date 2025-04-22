from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Vital, Threshold, Alert, Patient
from datetime import datetime, timedelta
import time

# Connect to existing database
engine = create_engine('sqlite:///patient_vitals.db')
Session = sessionmaker(bind=engine)
db = Session()

def get_threshold_range(patient):
    age = (datetime.now().date() - patient.date_of_birth.date()).days // 365
    gender = patient.gender.lower()
    
    threshold = db.query(Threshold).filter(
        Threshold.age_lower <= age,
        Threshold.age_upper >= age,
        Threshold.gender == gender
    ).first()
    
    return threshold

def detect_anomalies(patients):
    for patient in patients:
        threshold = get_threshold_range(patient)
        if not threshold:
            continue
        
        vitals = db.query(Vital).filter_by(patient_id=patient.id).order_by(Vital.timestamp.desc()).limit(10).all()
        vitals = list(reversed(vitals)) # oldest to newest
        
        consecutive_anomaly_flag = False
        consecutive_count = 0
        max_consecutive = 0

        for v in vitals:
            is_anomaly = (
                v.systolic < threshold.systolic_lower or v.systolic > threshold.systolic_upper or
                v.diastolic < threshold.diastolic_lower or v.diastolic > threshold.diastolic_upper or
                v.blood_sugar < threshold.blood_sugar_lower or v.blood_sugar > threshold.blood_sugar_upper or
                v.pulse_rate < threshold.pulse_rate_lower or v.pulse_rate > threshold.pulse_rate_upper or
                v.oxygen_volume < threshold.oxygen_levels_lower or v.oxygen_volume > threshold.oxygen_levels_upper
            )

            if is_anomaly:
                if consecutive_anomaly_flag:
                    consecutive_count += 1
                else:
                    consecutive_anomaly_flag = True
                    consecutive_count = 1
            else:
                # If normal, reset flag and counter
                consecutive_anomaly_flag = False
                consecutive_count = 0

            max_consecutive = max(max_consecutive, consecutive_count)

                
        if max_consecutive >= 10:
            alert = Alert(
                patient_id=patient.id,
                message="More than 10 anomalies detected! Critical!",
                severity="high",
                timestamp=datetime.now()
            )
            db.add(alert)
   
        elif max_consecutive >= 5:
            alert = Alert(
                patient_id=patient.id,
                message="More than 5 anomalies detected! Attention required!",
                severity="medium",
                timestamp=datetime.now()
            )
            db.add(alert)
            
        elif max_consecutive >= 2:
            alert = Alert(
                patient_id=patient.id,
                message="2 anomalies detected!",
                severity="low",
                timestamp=datetime.now()
            )
            db.add(alert)
        
    db.commit()
    
def run_anomaly_detection(patients):
    # patients = db.query(Patient).all()
    if not patients:
        print("No patients found.")
        return
    
    print("Starting continuous anomaly detection...")
    try:
        while True:
            detect_anomalies(patients)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped anomaly detection.")