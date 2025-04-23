from flask import Flask, request, jsonify, session, send_from_directory, redirect, render_template
from auth_utils import authenticate_staff, is_authorized_for_patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Staff, Patient, Vital
from report_details import fetch_patient_details
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder="../frontend")
app.secret_key = 'secret'

engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if methods == 'POST':
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
            return redirect('/patient_details_doctor')
        elif staff.role == "nurse":
            # go to patient_details_doctor
            return redirect('/patient_details_nurse')
        else:
            # Fallback in case role is not recognized
            return jsonify({'error': 'Unauthorized role'}), 403
        
    else:
        render_template('login.html')
    
    # return jsonify({'message': 'Login successful', 'role': staff.role}), 200
        
@app.route('/patient_details_nurse', methods=['POST'])
def patient_details_nurse():
    data = request.get_json()
    patient_id = data.get("patient_id")
    action = data.get("action")
    
    staff_id = session.get('staff_id')
    
    if not staff_id:
        return redirect('/login') # return to login page
    
    if is_authorized_for_patient(staff_id, patient_id):
        if action == "show_vitals":
            # redirect to vitals display page (graph)
            session['patient_id'] = patient_id
            return redirect('/graph')
        else:
            # redirect to login.html page
            return redirect('/login')
    else:
        # redirect to access_denied.html
        return redirect('/access_denied')
    
@app.route('/patient_details_doctor', methods=['POST'])
def patient_details_doctor():
    data = request.get_json()
    patient_id = data.get("patient_id")
    action = data.get("action")
    
    staff_id = session.get('staff_id')
    
    if not staff_id:
        return redirect('/login') # return to login page
    
    if is_authorized_for_patient(staff_id, patient_id):
        if action == "show_vitals":
            # redirect to vitals display page (graph)
            session['patient_id'] = patient_id
            return redirect('/graph')
        elif action == "patient_history":
            # redirect to patient_info page
            session['patient_id'] = patient_id
            return redirect('/patient_info')
        else:
            # redirect to login.html page
            return redirect('/login')
    else:
        # redirect to access_denied page
        return redirect('/access_denied')
    
    
@app.route('/graph', methods=['GET']) 
def display_vitals():
    patient_id = session.get('patient_id')
    
    if not patient_id:
        # redirect to prev page or login
        return redirect(request.referrer or '/login') 
    
    # fetch vitals of the past two hours from now
    two_hours_ago = datetime.now() - timedelta(hours=2)
    vitals = db.query(Vital).filter(Vital.patient_id == patient_id, Vital.timestamp >= two_hours_ago).all()
    
    # format vitals into dictionary
    if vitals:
        # Manually convert the vitals to dictionaries
        vitals_data = [{
            "id": v.id,
            "patient_id": v.patient_id,
            "systolic": v.systolic,
            "diastolic": v.diastolic,
            "pulse_rate": v.pulse_rate,
            "blood_sugar": v.blood_sugar,
            "oxygen_volume": v.oxygen_volume,
            "timestamp": v.timestamp.isoformat()  # Convert datetime to string
        } for v in vitals]

        return jsonify(vitals=vitals_data)
    else:
        return jsonify({'message': 'No vitals data available for the specified period'}), 404
    
@app.route('/patient_info', methods=['GET'])
def display_patient_info():
    patient_id = session.get('patient_id')
    
    if not patient_id:
        return redirect(request.referrer or '/login')
    
    try:
        data = fetch_patient_details(patient_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

