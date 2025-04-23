from static_data_gen import create_static_data
from vitals_gen import run_vitals_generation
from anomaly_detection import run_anomaly_detection
from threshold_data import create_thresholds

from multiprocessing import Process

if __name__ == "__main__":
    # Base data
    patients = create_static_data()
    create_thresholds()
    
    # Vitals generation and Anomaly detection
    vitals_proc = Process(target=run_vitals_generation, args=(patients,))
    anomaly_proc = Process(target=run_anomaly_detection, args=(patients,))
    
    vitals_proc.start()
    anomaly_proc.start()
    
    try:
        vitals_proc.join()
        anomaly_proc.join()
    except KeyboardInterrupt:
        print("Keyboard Interrupt received. Terminating process...")
        vitals_proc.terminate()
        anomaly_proc.terminate()
