from flask import Flask, request, jsonify, session
from auth_utils import authenticate_staff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Staff

app = Flask(__name__)
app.secret_key = 'secret'

engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    staff_id = data.get('staff_id')
    password = data.get('password')

    if not staff_id or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    staff = db.query(Staff).filter_by(id=staff_id).first()

    if not staff or not authenticate_staff(staff_id, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['staff_id'] = staff_id
    return jsonify({'message': 'Login successful', 'role': staff.role}), 200
        
