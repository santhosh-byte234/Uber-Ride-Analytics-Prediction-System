import os
import subprocess

# Export data for Power BI
def export_for_powerbi():
    import pandas as pd
    import mysql.connector
    
    conn = mysql.connector.connect(
        host='localhost',
        database='uber_analytics_db',
        user='root',
        password='Sandy@123'
    )
    
    df = pd.read_sql('SELECT * FROM rides', conn)
    df.to_csv('data/powerbi_export.csv', index=False)
    conn.close()
    
    print("Data exported for Power BI")

if __name__ == "__main__":
    export_for_powerbi()
