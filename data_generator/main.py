# ==============================================================================
# Customer Support Operations Intelligence Platform - Main Data Generator CLI
# ==============================================================================

import os
import argparse
import yaml
import pandas as pd
from datetime import datetime, timedelta

from data_generator.generators.customers import generate_customers
from data_generator.generators.agents import generate_agents
from data_generator.generators.tickets import generate_tickets_and_events

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic customer support operations data.")
    parser.add_argument("--customers", type=int, default=1000, help="Number of customers to generate")
    parser.add_argument("--agents", type=int, default=50, help="Number of support agents to generate")
    parser.add_argument("--days", type=int, default=365, help="Number of days of history to generate")
    parser.add_argument("--config", type=str, default="data_generator/config/correlations.yaml", help="Path to config file")
    parser.add_argument("--output-dir", type=str, default="data_generator/output", help="Directory to save generated CSVs")
    
    args = parser.parse_args()
    
    print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    
    # Define date range
    # Timeline ends yesterday
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days)
    
    print(f"Generating data from {start_date} to {end_date} ({args.days} days)...")
    
    # 1. Generate Customers
    print(f"Generating {args.customers} customers...")
    customers = generate_customers(args.customers, start_date, end_date)
    
    # 2. Generate  AI Agents
    print(f"Generating {args.agents} agents...")
    agents = generate_agents(args.agents, start_date)
    
    # 3. Generate Tickets, Events, and Capacity
    print("Generating tickets, lifecycle events, and agent daily capacity records...")
    tickets, events, capacity = generate_tickets_and_events(
        customers, agents, start_date, end_date, config
    )
    
    # Convert to DataFrames
    df_customers = pd.DataFrame(customers)
    df_agents = pd.DataFrame(agents)
    df_tickets = pd.DataFrame(tickets)
    df_events = pd.DataFrame(events)
    df_capacity = pd.DataFrame(capacity)
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Write to CSV
    print(f"Saving generated datasets to {args.output_dir}...")
    df_customers.to_csv(os.path.join(args.output_dir, "customers.csv"), index=False)
    df_agents.to_csv(os.path.join(args.output_dir, "agents.csv"), index=False)
    df_tickets.to_csv(os.path.join(args.output_dir, "tickets.csv"), index=False)
    df_events.to_csv(os.path.join(args.output_dir, "ticket_events.csv"), index=False)
    df_capacity.to_csv(os.path.join(args.output_dir, "agent_daily_capacity.csv"), index=False)
    
    # Create empty .gitkeep in output folder to track it but ignore CSVs
    with open(os.path.join(args.output_dir, ".gitkeep"), 'w') as f:
        pass
        
    print("Data generation complete!")
    print(f"Summary of generated data:")
    print(f"  - Customers: {len(df_customers)}")
    print(f"  - Agents: {len(df_agents)}")
    print(f"  - Tickets: {len(df_tickets)}")
    print(f"  - Ticket Events: {len(df_events)}")
    print(f"  - Agent Daily Capacity Records: {len(df_capacity)}")

if __name__ == "__main__":
    main()
