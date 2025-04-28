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


# Future enhancements
# Contributions
