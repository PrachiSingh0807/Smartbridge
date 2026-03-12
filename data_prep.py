import pandas as pd
import sqlite3
import os

def prep_data(csv_file='dataset.csv', db_file='database.db'):
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Please run generate_sample_data.py first.")
        return

    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)

    # The Kaggle dataset format usually has Date as the index/first column and States as other columns.
    # We will unpivot (melt) it into a format easier for SQL & Tableau: [Date, State, Consumption]
    df_melted = df.melt(id_vars=['Date'], var_name='State', value_name='Consumption')
    
    # Convert string dates to actual datetime objects for better SQL querying/sorting
    df_melted['Date'] = pd.to_datetime(df_melted['Date']).dt.date

    print(f"Connecting to {db_file}...")
    conn = sqlite3.connect(db_file)
    
    # Write to SQLite, replacing existing table
    df_melted.to_sql('electricity_consumption', conn, if_exists='replace', index=False)
    
    # Create indexes for faster queries
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON electricity_consumption (Date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_state ON electricity_consumption (State)")
    conn.commit()

    print(f"Successfully loaded {len(df_melted)} records into {db_file}.")
    conn.close()

if __name__ == "__main__":
    prep_data()
