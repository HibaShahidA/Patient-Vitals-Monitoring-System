from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Threshold

engine = create_engine("sqlite:///patient_vitals.db")
Session = sessionmaker(bind=engine)
db = Session()

def create_thresholds():
    thresholds = [
        # Infants (0-1 years)
        Threshold(age_lower=0, age_upper=1, gender="male",
                  systolic_lower=70, systolic_upper=100,
                  diastolic_lower=50, diastolic_upper=65,
                  blood_sugar_lower=60.0, blood_sugar_upper=100.0,
                  pulse_rate_lower=100, pulse_rate_upper=160,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=0, age_upper=1, gender="female",
                  systolic_lower=70, systolic_upper=100,
                  diastolic_lower=50, diastolic_upper=65,
                  blood_sugar_lower=60.0, blood_sugar_upper=100.0,
                  pulse_rate_lower=100, pulse_rate_upper=160,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),

        # Toddlers (1-3 years)
        Threshold(age_lower=1, age_upper=3, gender="male",
                  systolic_lower=80, systolic_upper=110,
                  diastolic_lower=55, diastolic_upper=70,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=90, pulse_rate_upper=150,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=1, age_upper=3, gender="female",
                  systolic_lower=80, systolic_upper=110,
                  diastolic_lower=55, diastolic_upper=70,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=90, pulse_rate_upper=150,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),

        # Children (4-12 years)
        Threshold(age_lower=4, age_upper=12, gender="male",
                  systolic_lower=85, systolic_upper=120,
                  diastolic_lower=60, diastolic_upper=75,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=70, pulse_rate_upper=110,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=4, age_upper=12, gender="female",
                  systolic_lower=85, systolic_upper=120,
                  diastolic_lower=60, diastolic_upper=75,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=70, pulse_rate_upper=110,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),

        # Adolescents (13-18 years)
        Threshold(age_lower=13, age_upper=18, gender="male",
                  systolic_lower=90, systolic_upper=130,
                  diastolic_lower=65, diastolic_upper=80,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=13, age_upper=18, gender="female",
                  systolic_lower=90, systolic_upper=130,
                  diastolic_lower=65, diastolic_upper=80,
                  blood_sugar_lower=70.0, blood_sugar_upper=110.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),

        # Adults (19-64 years)
        Threshold(age_lower=19, age_upper=64, gender="male",
                  systolic_lower=90, systolic_upper=140,
                  diastolic_lower=60, diastolic_upper=90,
                  blood_sugar_lower=70.0, blood_sugar_upper=120.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=19, age_upper=64, gender="female",
                  systolic_lower=90, systolic_upper=140,
                  diastolic_lower=60, diastolic_upper=90,
                  blood_sugar_lower=70.0, blood_sugar_upper=120.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=95.0, oxygen_levels_upper=100.0),

        # Seniors (65+ years)
        Threshold(age_lower=65, age_upper=120, gender="male",
                  systolic_lower=100, systolic_upper=150,
                  diastolic_lower=60, diastolic_upper=90,
                  blood_sugar_lower=70.0, blood_sugar_upper=130.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=93.0, oxygen_levels_upper=100.0),
        Threshold(age_lower=65, age_upper=120, gender="female",
                  systolic_lower=100, systolic_upper=150,
                  diastolic_lower=60, diastolic_upper=90,
                  blood_sugar_lower=70.0, blood_sugar_upper=130.0,
                  pulse_rate_lower=60, pulse_rate_upper=100,
                  oxygen_levels_lower=93.0, oxygen_levels_upper=100.0),
    ]
    db.add_all(thresholds)
    db.commit()

# if __name__ == "__main__":
#     engine = create_engine("sqlite:///patient_vitals.db")
#     Session = sessionmaker(bind=engine)
#     db = Session()

#     # Create the table if not already created
#     Base.metadata.create_all(engine)

#     # Only add thresholds if the table is empty (to avoid duplicates)
#     if db.query(Threshold).count() == 0:
#         create_thresholds(db)
#         print("Thresholds created.")
#     else:
#         print("Thresholds already exist.")