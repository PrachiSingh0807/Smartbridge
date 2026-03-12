import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(filename='dataset.csv'):
    print(f"Generating synthetic dataset: {filename}...")
    
    # Date range: Jan 1, 2019 to Dec 31, 2020
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2020, 12, 31)
    delta = end_date - start_date
    dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    
    # List of Indian States
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", 
        "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
        "Uttarakhand", "West Bengal", "Delhi"
    ]
    
    # Base consumption factors to simulate realistic regional variations
    base_factors = {state: np.random.uniform(50, 400) for state in states}
    
    # Heavy industrial states have higher consumption
    high_consumers = ["Maharashtra", "Gujarat", "Tamil Nadu", "Uttar Pradesh", "Karnataka"]
    for state in high_consumers:
        base_factors[state] += 200

    data = {'Date': [d.strftime('%Y-%m-%d') for d in dates]}
    
    for state in states:
        base = base_factors[state]
        consumption = []
        for d in dates:
            # Seasonal factor: higher in summer (April-June), lower in winter
            month = d.month
            seasonal = 1.2 if 4 <= month <= 6 else (0.9 if 11 <= month <= 2 else 1.0)
            
            # COVID Lockdown effect (March 24, 2020 to June 30, 2020)
            covid_effect = 1.0
            if d >= datetime(2020, 3, 24) and d <= datetime(2020, 6, 30):
                covid_effect = 0.75 # 25% drop during strict lockdown
                
            # Recovery phase
            if d > datetime(2020, 6, 30):
                covid_effect = min(1.0, 0.75 + (d - datetime(2020, 6, 30)).days * 0.002)
                
            daily_noise = np.random.uniform(-10, 10)
            val = base * seasonal * covid_effect + daily_noise
            consumption.append(max(0, round(val, 2))) # Ensure non-negative
            
        data[state] = consumption

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Dataset securely saved as {filename}")

if __name__ == "__main__":
    generate_synthetic_data()
