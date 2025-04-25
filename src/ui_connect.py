from flask import Flask, request, jsonify, session, send_from_directory, redirect, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Staff, Patient, Vital, Alert, PatientStaff
from report_details import fetch_patient_details
from auth_utils import authenticate_staff, is_authorized_for_patient
from graph_utils import generate_graph_data
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
app.secret_key = 'secret'

engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        staff_id = data.get('staff_id')
        password = data.get('password')

        if not staff_id or not password:
            return jsonify({'error': 'Missing credentials'}), 400

        staff = db.query(Staff).filter_by(id=staff_id).first()

        if not staff or not authenticate_staff(staff_id, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session['staff_id'] = staff_id
        
        if staff.role == "doctor":
            # go to patient_details_doctor
            return jsonify({'redirect': '/patient_details_doctor'})
        elif staff.role == "nurse" or staff.role == "head_nurse":
            # go to patient_details_doctor
            return jsonify({'redirect': '/patient_details_nurse'})
        else:
            # Fallback in case role is not recognized
            return jsonify({'error': 'Unauthorized role'}), 403
        
    else:
        return render_template('login.html')
    
    # return jsonify({'message': 'Login successful', 'role': staff.role}), 200
    
        
@app.route('/patient_details_nurse', methods=['GET', 'POST'])
def patient_details_nurse():
    if request.method == 'POST':
        data = request.get_json()
        patient_id = data.get("patient_id")
        action = data.get("action")
        
        staff_id = session.get('staff_id')
        
        if not staff_id:
            return jsonify({'redirect': '/login'}) # return to login page
        
        if action == 'log_out':
            # redirect to login.html page
            session.clear()
            return jsonify({'redirect': '/login'})
        
        if action == 'acknowledge_alert':
            return jsonify({'redirect': '/graphs'})
        
        if is_authorized_for_patient(staff_id, patient_id):
            if action == 'show_vitals':
                # redirect to vitals display page (graph)
                session['patient_id'] = patient_id
                return jsonify({'redirect': '/graphs'})
            else:
                # redirect to login.html page
                return jsonify({'redirect': '/login'})
        else:
            # redirect to access_denied.html
            return jsonify({'redirect': '/access_denied'})
        
    else:
        return render_template('patient_details_nurse.html')
    
    
@app.route('/patient_details_doctor', methods=['GET', 'POST'])
def patient_details_doctor():
    if request.method == 'POST':
        data = request.get_json()
        patient_id = data.get("patient_id")
        action = data.get("action")
        
        staff_id = session.get('staff_id')
        
        if not staff_id:
            return jsonify({'redirect': '/login'}) # return to login page
        
        if action == 'log_out':
            # redirect to login.html page
            session.clear()
            return jsonify({'redirect': '/login'})
        
        if action == 'acknowledge_alert':
            return jsonify({'redirect': '/graphs'})
        
        if is_authorized_for_patient(staff_id, patient_id):
            if action == "show_vitals":
                # redirect to vitals display page (graph)
                session['patient_id'] = patient_id
                return jsonify({'redirect': '/graphs'})
                
            elif action == "patient_history":
                # redirect to patient_info page
                session['patient_id'] = patient_id
                return jsonify({'redirect': '/patient_info'})
                
            else:
                # redirect to login.html page
                return jsonify({'redirect': '/login'})
                
        else:
            # redirect to access_denied page
            return jsonify({'redirect': '/access_denied'})
            
    else:
        return render_template('patient_details_doctor.html')
    
        
@app.route('/graphs', methods=['GET']) 
def graphs_page():
    return render_template('graphs.html')


@app.route('/get_vitals', methods=['GET'])
def display_vitals():
    patient_id = session.get('patient_id')
    
    if not patient_id:
        # redirect to prev page or login
        return redirect(request.referrer or '/login') 
    
    # fetch vitals of the patient
    data = generate_graph_data(patient_id)
    patient = db.query(Patient).filter_by(id=patient_id).first()
    if data:
        return jsonify({
            "vitals": data["vitals"],
            "thresholds": data["thresholds"],
            "patient_name": f"{patient.name}"
        })
    else:
        return jsonify({
            "vitals": [],
            "thresholds": {},
            "message": "No vitals data available for the specified period"
        }), 200
    
    
@app.route('/patient_info', methods=['GET', 'POST'])
def display_patient_info():
    if request.method == 'POST':
        referrer = request.referrer
        if referrer and '/patient_info' not in referrer:
            return jsonify({'redirect': referrer})
        else:   
            staff_id = session.get('staff_id')
            staff = db.query(Staff).filter_by(id=staff_id).first()
            role = staff.role
            if role == "doctor":
                return jsonify({'redirect': '/patient_details_doctor'})
            elif role == "nurse" or role == "head_nurse":
                return jsonify({'redirect': '/patient_details_nurse'})
            else:
                return jsonify({'redirect': '/login'})
    else:
        patient_id = session.get('patient_id')
        
        if not patient_id:
            return jsonify({'redirect': '/login'})  # Redirect if there's no patient ID

        try:
            data = fetch_patient_details(patient_id)  # Fetch the patient details
            
            return render_template('patient_info.html', patient_info=data)  # Pass the data to the template
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
@app.route('/access_denied', methods=['GET', 'POST'])
def deny_access():
    if request.method == 'POST':
        referrer = request.referrer
        if referrer and '/access_denied' not in referrer:
            return jsonify({'redirect': referrer})
        else:   
            staff_id = session.get('staff_id')
            staff = db.query(Staff).filter_by(id=staff_id).first()
            role = staff.role
            if role == "doctor":
                return jsonify({'redirect': '/patient_details_doctor'})
            elif role == "nurse" or role == "head_nurse":
                return jsonify({'redirect': '/patient_details_nurse'})
            else:
                return jsonify({'redirect': '/login'})
    else:
        return render_template('access_denied.html')
    
    
@app.route('/get_alerts', methods=['GET'])
def check_alerts():
    staff_id = session.get('staff_id')
    if not staff_id:
        return jsonify({"alert": None}), 401

    ten_minutes_ago = datetime.now() - timedelta(minutes=10)

    # Find all patients assigned to this staff member
    assigned_patients = db.query(PatientStaff).filter_by(staff_id=staff_id).all()
    alerts = []

    for ps in assigned_patients:
        if is_authorized_for_patient(staff_id, ps.patient_id):
            patient_id = ps.patient_id

            # Look for high-severity alerts in the last 10 minutes
            recent_critical_alert = db.query(Alert).filter(
                Alert.patient_id == patient_id,
                Alert.severity == "high",
                Alert.timestamp >= ten_minutes_ago
            ).order_by(Alert.timestamp.desc()).first()

            if recent_critical_alert:
                patient = db.query(Patient).filter_by(id=patient_id).first()
                alerts.append({
                    "patient_id": patient.id,
                    "patient_name": patient.name,
                    "message": recent_critical_alert.message,
                    "severity": recent_critical_alert.severity,
                    "timestamp": recent_critical_alert.timestamp.isoformat()
                })

    if alerts:
        return jsonify({"alert": alerts})  # Return all alerts
    else:
        return jsonify({"alert": None})

# @app.route('/mark_alert_seen', methods=['POST'])
# def mark_alert_seen():
#     data = request.get_json()
#     alert_id = data.get('alert_id')
    
#     # Fetch the alert from the database
#     alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
#     if alert:
#         return jsonify({'message': 'Alert marked as seen', 'redirect': '/graph'})
#     else:
#         return jsonify({'error': 'Alert not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
