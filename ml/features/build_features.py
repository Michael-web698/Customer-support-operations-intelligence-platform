# ==============================================================================
# Customer Support Operations Intelligence Platform - Feature Engineering
# ==============================================================================

import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_db_connection():
    load_dotenv()
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "support_ops_intel")
    
    connection_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    try:
        engine = create_engine(connection_url)
        return engine
    except Exception as e:
        print(f"Database connection failed in ML feature engineering: {e}", file=sys.stderr)
        sys.exit(1)

def load_ticket_features(engine):
    """
    Loads ticket features from marts fact_ticket and joined dimensions for classification and risk models.
    """
    query = """
        select
            f.ticket_id,
            f.subject,
            f.description,
            coalesce(f.subject, '') || ' ' || coalesce(f.description, '') as ticket_text,
            c.category_name as ground_truth_category,
            f.priority as ground_truth_priority,
            cust.segment as customer_segment,
            cust.region as customer_region,
            f.channel_key,
            ch.channel_name,
            a.seniority_level as agent_seniority_level,
            a.team as agent_team,
            extract(hour from f.created_at) as creation_hour,
            f.reopened_count,
            f.is_escalated,
            -- Sentiment logic placeholder (can extract actual target labels for evaluation)
            case
                when f.csat_score in (4, 5) then 'Positive'
                when f.csat_score = 3 then 'Neutral'
                when f.csat_score in (1, 2) then 'Negative'
                else 'Neutral' -- default placeholder
            end as ground_truth_sentiment
        from marts.fact_ticket f
        join marts.dim_category c on f.category_key = c.category_key
        join marts.dim_customer cust on f.customer_id = cust.customer_id
        join marts.dim_channel ch on f.channel_key = ch.channel_key
        join marts.dim_agent a on f.agent_id = a.agent_id
    """
    print("Loading ticket feature records from marts schema...")
    df = pd.read_sql(query, con=engine)
    return df

def load_daily_volume_features(engine):
    """
    Loads daily historical ticket volume records for forecasting.
    """
    query = """
        select
            date_day::date as date_day,
            sum(ticket_count) as total_ticket_count
        from marts.fact_daily_ticket_volume
        group by 1
        order by 1 asc
    """
    print("Loading daily aggregated volume records for time-series forecasting...")
    df = pd.read_sql(query, con=engine)
    return df
