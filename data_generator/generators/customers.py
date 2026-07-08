# ==============================================================================
# Customer Support Operations Intelligence Platform - Customer Data Generator
# ==============================================================================

import random
from datetime import timedelta

REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America"]

def generate_customers(num_customers, start_date, end_date):
    """
    Generates a list of customers with segment, region, signup_date, and plan_tier.
    """
    customers = []
    
    # Segment distribution weights
    segments = ["Free", "Pro", "Enterprise"]
    segment_weights = [0.60, 0.30, 0.10]
    
    date_range_days = (end_date - start_date).days
    
    for i in range(1, num_customers + 1):
        customer_id = i
        segment = random.choices(segments, weights=segment_weights)[0]
        region = random.choice(REGIONS)
        
        # Signup date is randomly spread over the timeline (or slightly before)
        # Some customers signed up before the timeline starts
        days_offset = random.randint(-180, date_range_days)
        signup_date = start_date + timedelta(days=days_offset)
        
        # Plan tier matches segment
        if segment == "Free":
            plan_tier = "Basic"
        elif segment == "Pro":
            plan_tier = "Professional"
        else:
            plan_tier = "Enterprise"
            
        customers.append({
            "customer_id": customer_id,
            "segment": segment,
            "region": region,
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "plan_tier": plan_tier
        })
        
    return customers
