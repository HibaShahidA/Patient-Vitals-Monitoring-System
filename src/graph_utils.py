from models import Patient, Vital
from anomaly_detection import get_threshold_range
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Setup database connection
engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

def generate_graph_data(patient_id):
    ''' fetches and processes necessary patient data '''
    two_hours_ago = datetime.now() - timedelta(hours=2)
    
    vitals = db.query(Vital).filter(
        Vital.patient_id == patient_id,
        Vital.timestamp >= two_hours_ago
    ).all()

    vitals_data = [{
        "id": v.id,
        "patient_id": v.patient_id,
        "systolic": v.systolic,
        "diastolic": v.diastolic,
        "pulse_rate": v.pulse_rate,
        "blood_sugar": v.blood_sugar,
        "oxygen_volume": v.oxygen_volume,
        "timestamp": v.timestamp.isoformat()
    } for v in vitals]
    
    patient = db.query(Patient).filter_by(id=patient_id).first()
    thresholds = get_threshold_range(patient)

    return {
        "vitals": vitals_data,
        "thresholds": thresholds
    }
    
    
def plot_graph(data):
    ''' prepares the graphs with appropriate data '''
    temp=0