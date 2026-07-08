# ==============================================================================
# Customer Support Operations Intelligence Platform - Raw Ingestion Pipeline
# ==============================================================================

import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "support_ops_intel")
    
    csv_dir = "data_generator/output"
    
    # Establish connection
    connection_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(f"Connecting to database {db_name} at {db_host}:{db_port}...")
    
    try:
        engine = create_engine(connection_url)
        # Create raw schema
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.commit()
            print("Schema 'raw' verified/created.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}", file=sys.stderr)
        sys.exit(1)
        
    datasets = {
        "customers.csv": "raw_customers",
        "agents.csv": "raw_agents",
        "tickets.csv": "raw_tickets",
        "ticket_events.csv": "raw_ticket_events",
        "agent_daily_capacity.csv": "raw_agent_daily_capacity"
    }
    
    for file_name, table_name in datasets.items():
        file_path = os.path.join(csv_dir, file_name)
        if not os.path.exists(file_path):
            print(f"Error: Source file {file_path} not found. Run generator first.", file=sys.stderr)
            sys.exit(1)
            
        print(f"Reading {file_path}...")
        df = pd.read_csv(file_path)
        
        # Load into raw schema
        print(f"Ingesting into raw.{table_name} ({len(df)} rows)...")
        try:
            df.to_sql(
                name=table_name,
                con=engine,
                schema="raw",
                if_exists="replace",
                index=False,
                method="multi", # Batch insert
                chunksize=10000
            )
            print(f"Successfully loaded raw.{table_name}")
        except Exception as e:
            print(f"Failed to load table raw.{table_name}: {e}", file=sys.stderr)
            sys.exit(1)
            
    print("All raw tables successfully ingested!")

if __name__ == "__main__":
    main()
