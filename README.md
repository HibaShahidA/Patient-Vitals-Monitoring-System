# Patient-Vitals-Monitoring-System

# Overview
The Patient Vitals Monitoring System is designed to track and display real-time health data for patients, including vital signs such as heart rate, blood pressure, body temperature, and oxygen saturation. The system provides a dashboard for healthcare professionals to monitor patient status and receive alerts when vitals exceed safe thresholds.

# Features
- Real-time monitoring of multiple patients
- Display of vitals: heart rate, blood pressure, temperature, SpO₂
- Alert system for abnormal readings
- Historical data tracking and visualization
- Scalable and modular architecture

# Tech Stack
- Frontend: HTML, CSS
- Backend: Python
- Database: SQLAlchemy, SQLite

# Dataset
The data set used for testing is collected through multiple resources, such as:
- synthetic data auto-created using random data generation
- real-life data from multiple medical sources (to be edited as per use)

# Set-up instructions

## 1. Install Dependencies
Install all required Python packages by running:
```bash
pip install --no-cache-dir -r requirements.txt
```

## 2. Start the Data Generation Service
Open a terminal and run:
```bash
python3 src/data_gen_main.py
```

## 3. Start the Web Application
Open another terminal and run:
```bash
python3 src/ui_connect.py
```

## 4. Access the Application
- After starting `ui_connect.py`, a link will appear in the terminal (e.g., `http://127.0.0.1:5001`).
- Open your browser, paste the link into the address bar, and append `/login` at the end.
  Example:
  ```bash
  http://127.0.0.1:5001/login
  ```

# Folder Structure

- `frontend/`
  - `access_denied.html`
  - `alert.html`
  - `graphs.html`
  - `login.html`
  - `patient_details_doctor.html`
  - `patient_details_nurse.html`
  - `patient_info.html`
  - `styles.css`
  
- `src/`
  - `anomaly_detection.py`
  - `auth_utils.py`
  - `data_gen_main.py`
  - `db_connect.py`
  - `graph_utils.py`
  - `models.py`
  - `notes.txt`
  - `report_details.py`
  - `static_data_gen.py`
  - `threshold_data.py`
  - `ui_connect.py`
  - `vitals_gen.py`
  
- `documentation/`
  - `SRS.pdf`
  - `SDS.pdf`
  
- `requirements.txt`

# Future Enhancements

- **Frontend Improvements**  
  Replace the current raw HTML with a modern frontend framework (e.g., React, Vue.js, or a UI library like Bootstrap) for a more responsive and user-friendly interface.

- **Backend and Database Improvements**  
  Upgrade the backend structure and migrate from SQLite to a more robust database solution such as PostgreSQL or MySQL.

- **Scalability**  
  Refactor the project to create a scalable version that can support deployment in real-world hospital environments, handling more patients, staff, and real-time data efficiently.

- **Authentication and Authorization**  
  Implement secure role-based access control for staff (e.g., doctors, nurses, admins) to protect sensitive patient data.

- **Alert Notification System**  
  Develop real-time alerts (e.g., in-app popups or email notifications) when patient vitals cross critical thresholds.

- **Analytics Dashboard**  
  Create a dashboard displaying patient trends, vitals statistics, and system-wide health insights.

# Contributions

- **Fatima Hassan** — Frontend development, frontend logic, wireframes
- **Aiman Rizwan** — Documentation (SRS, SDS)
- **Hiba Shahid** — Backend development (data generation, database, server logic)
