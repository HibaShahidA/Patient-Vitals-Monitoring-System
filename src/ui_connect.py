from flask import Flask, request, jsonify, session, send_from_directory, redirect, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Staff, Patient, Vital
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
        elif staff.role == "nurse":
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
        
        if is_authorized_for_patient(staff_id, patient_id):
            if action == 'show_vitals':
                # redirect to vitals display page (graph)
                session['patient_id'] = patient_id
                return jsonify({'redirect': '/graph'})
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
        
        if is_authorized_for_patient(staff_id, patient_id):
            if action == "show_vitals":
                # redirect to vitals display page (graph)
                session['patient_id'] = patient_id
                return jsonify({'redirect': '/graph'})
                
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
    
        
@app.route('/graph', methods=['GET']) 
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
