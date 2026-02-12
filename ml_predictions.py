from sqlalchemy import create_engine
import pandas as pd

def load_data_from_mysql():
    # SQLAlchemy connection string: 'mysql+pymysql://user:password@host/database'
    engine = create_engine('mysql+pymysql://root:Sandy@123@localhost/uber_analytics_db')
    
    query = """
        SELECT 
            HOUR(start_date) as hour,
            DAYOFWEEK(start_date) as day_of_week,
            MONTH(start_date) as month,
            miles,
            category
        FROM rides
    """
    df = pd.read_sql(query, engine)
    
    if df.empty:
        raise ValueError("No data found in 'rides' table. Please import data before training the model.")
    
    return df
