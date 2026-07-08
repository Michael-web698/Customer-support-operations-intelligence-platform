# ==============================================================================
# Customer Support Operations Intelligence Platform - Raw Data Quality Checks
# ==============================================================================

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def run_query(conn, sql_query):
    result = conn.execute(text(sql_query))
    return result.fetchall()

def main():
    load_dotenv()
    
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "support_ops_intel")
    
    connection_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    print(f"Connecting to database to run quality checks...")
    
    try:
        engine = create_engine(connection_url)
        conn = engine.connect()
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)
        
    failures = 0
    
    # 1. Row count validations
    tables = [
        "raw_customers",
        "raw_agents",
        "raw_tickets",
        "raw_ticket_events",
        "raw_agent_daily_capacity"
    ]
    
    print("\n--- Running Row Count Quality Checks ---")
    for table in tables:
        try:
            res = run_query(conn, f"SELECT COUNT(*) FROM raw.{table};")
            count = res[0][0]
            if count > 0:
                print(f" [PASS] raw.{table} has {count} rows.")
            else:
                print(f" [FAIL] raw.{table} is empty!")
                failures += 1
        except Exception as e:
            print(f" [FAIL] Failed to query raw.{table}: {e}")
            failures += 1
            
    # 2. Uniqueness & Nullability checks on Primary Keys
    print("\n--- Running Primary Key Quality Checks ---")
    pk_checks = {
        "raw_customers": "customer_id",
        "raw_agents": "agent_id",
        "raw_tickets": "ticket_id",
        "raw_ticket_events": "event_id"
    }
    
    for table, pk in pk_checks.items():
        # Check Nulls
        null_query = f"SELECT COUNT(*) FROM raw.{table} WHERE {pk} IS NULL;"
        nulls = run_query(conn, null_query)[0][0]
        if nulls == 0:
            print(f" [PASS] raw.{table}.{pk} has 0 NULLs.")
        else:
            print(f" [FAIL] raw.{table}.{pk} has {nulls} NULL values!")
            failures += 1
            
        # Check Uniqueness
        dup_query = f"SELECT COUNT(*) FROM (SELECT {pk} FROM raw.{table} GROUP BY {pk} HAVING COUNT(*) > 1) AS dups;"
        dups = run_query(conn, dup_query)[0][0]
        if dups == 0:
            print(f" [PASS] raw.{table}.{pk} is unique.")
        else:
            print(f" [FAIL] raw.{table}.{pk} contains duplicate entries!")
            failures += 1
            
    # Composite PK check for capacity
    capacity_null_query = "SELECT COUNT(*) FROM raw.raw_agent_daily_capacity WHERE agent_id IS NULL OR date IS NULL;"
    nulls = run_query(conn, capacity_null_query)[0][0]
    if nulls == 0:
         print(" [PASS] raw.raw_agent_daily_capacity composite keys are non-null.")
    else:
         print(f" [FAIL] raw.raw_agent_daily_capacity has composite key NULL values!")
         failures += 1
         
    capacity_dup_query = "SELECT COUNT(*) FROM (SELECT agent_id, date FROM raw.raw_agent_daily_capacity GROUP BY agent_id, date HAVING COUNT(*) > 1) AS dups;"
    dups = run_query(conn, capacity_dup_query)[0][0]
    if dups == 0:
         print(" [PASS] raw.raw_agent_daily_capacity composite keys are unique.")
    else:
         print(" [FAIL] raw.raw_agent_daily_capacity composite keys contain duplicate entries!")
         failures += 1
         
    # 3. Relationship Referrals Checks (Foreign Keys)
    print("\n--- Running Referential Integrity Quality Checks ---")
    
    # tickets -> customers
    cust_fk_query = "SELECT COUNT(*) FROM raw.raw_tickets t LEFT JOIN raw.raw_customers c ON t.customer_id = c.customer_id WHERE c.customer_id IS NULL;"
    orphans = run_query(conn, cust_fk_query)[0][0]
    if orphans == 0:
        print(" [PASS] All ticket customer_ids exist in raw_customers.")
    else:
        print(f" [FAIL] Found {orphans} ticket customer_ids not matching raw_customers!")
        failures += 1
        
    # tickets -> agents
    agent_fk_query = "SELECT COUNT(*) FROM raw.raw_tickets t LEFT JOIN raw.raw_agents a ON t.assigned_agent_id = a.agent_id WHERE a.agent_id IS NULL;"
    orphans = run_query(conn, agent_fk_query)[0][0]
    if orphans == 0:
        print(" [PASS] All ticket assigned_agent_ids exist in raw_agents.")
    else:
        print(f" [FAIL] Found {orphans} ticket assigned_agent_ids not matching raw_agents!")
        failures += 1
        
    # events -> tickets
    event_fk_query = "SELECT COUNT(*) FROM raw.raw_ticket_events e LEFT JOIN raw.raw_tickets t ON e.ticket_id = t.ticket_id WHERE t.ticket_id IS NULL;"
    orphans = run_query(conn, event_fk_query)[0][0]
    if orphans == 0:
        print(" [PASS] All event ticket_ids exist in raw_tickets.")
    else:
        print(f" [FAIL] Found {orphans} event ticket_ids not matching raw_tickets!")
        failures += 1
        
    conn.close()
    
    print("\n--- Quality Checks Summary ---")
    if failures == 0:
        print("🎉 ALL DATA QUALITY CHECKS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"❌ DATA QUALITY CHECKS FAILED WITH {failures} ERRORS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
