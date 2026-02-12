import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
from mysql.connector import Error

def load_and_clean_data(file_path):
    """Load and clean Uber dataset"""
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    # Handle missing values
    df['PURPOSE'].fillna('NOT', inplace=True)
    
    # Convert to datetime
    df['START_DATE'] = pd.to_datetime(df['START_DATE'])
    df['END_DATE'] = pd.to_datetime(df['END_DATE'])
    
    # Extract time features
    df['date'] = df['START_DATE'].dt.date
    df['hour'] = df['START_DATE'].dt.hour
    df['day_of_week'] = df['START_DATE'].dt.dayofweek
    df['month'] = df['START_DATE'].dt.month
    df['year'] = df['START_DATE'].dt.year
    
    # Create day period categories
    df['time_period'] = pd.cut(df['hour'], 
                                bins=[0, 6, 12, 18, 24],
                                labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    
required_cols = ['START_DATE', 'END_DATE', 'CATEGORY', 'START', 'STOP', 'MILES', 'PURPOSE', 'DRIVER']
for col in required_cols:
    if col not in df.columns:
        if col == 'DRIVER':
            df[col] = 'Kumar'
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Remove null rows
    df.dropna(inplace=True)
    
    print(f"Data cleaned. Total rides: {len(df)}")
    return df

def connect_to_database():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='uber_analytics_db',
            user='root',
            password='Sandy@123'  # Change this
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def import_to_mysql(df, connection):
    """Import cleaned data to MySQL"""
    cursor = connection.cursor()
    
    for _, row in df.iterrows():
        sql = """INSERT INTO rides 
                 (start_date, end_date, category, start_location, 
                  end_location, miles, purpose) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (row['START_DATE'], row['END_DATE'], row['CATEGORY'],
                 row['START'], row['STOP'], row['MILES'], row['PURPOSE'])
        cursor.execute(sql, values)
    
    connection.commit()
    print(f"{cursor.rowcount} records inserted into MySQL")
    cursor.close()

# Main execution
if __name__ == "__main__":
    # Load and clean data
    df = load_and_clean_data('data/UberDataset.csv')
    
    # Save cleaned data
    df.to_csv('data/UberDataset_cleaned.csv', index=False)
    
    # Connect to MySQL
    conn = connect_to_database()
    
    if conn:
        # Import to MySQL
        import_to_mysql(df, conn)
        conn.close()
        print("Data import completed!")
