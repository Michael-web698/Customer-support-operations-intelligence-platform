# ==============================================================================
# Customer Support Operations Intelligence Platform - Agent Data Generator
# ==============================================================================

import random
from datetime import timedelta

FIRST_NAMES = ["John", "Emily", "Michael", "Jessica", "David", "Sarah", "James", "Ashley", "Robert", "Amanda", 
               "William", "Megan", "Joseph", "Stephanie", "Matthew", "Nicole", "Daniel", "Elizabeth", "Christopher", "Rachel"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]

TEAMS = ["Billing Team", "Technical Support Team", "Account Management", "Customer Success"]
SHIFTS = ["Day", "Swing", "Night"]
STATUSES = ["Full-time", "Part-time", "Contract"]

def generate_agents(num_agents, start_date):
    """
    Generates a list of agents with seniority, shift, team, and hire_date.
    """
    agents = []
    
    # Seniority distributions
    seniorities = ["Junior", "Mid", "Senior"]
    seniority_weights = [0.40, 0.40, 0.20] # 40% Junior, 40% Mid, 20% Senior
    
    for i in range(1, num_agents + 1):
        agent_id = i
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        seniority = random.choices(seniorities, weights=seniority_weights)[0]
        team = random.choice(TEAMS)
        shift = random.choice(SHIFTS)
        status = random.choice(STATUSES)
        
        # Hire date is spread out up to 2 years before the timeline starts
        days_offset = random.randint(-730, -30)
        hire_date = start_date + timedelta(days=days_offset)
        
        agents.append({
            "agent_id": agent_id,
            "name": name,
            "team": team,
            "seniority_level": seniority,
            "hire_date": hire_date.strftime("%Y-%m-%d"),
            "shift": shift,
            "employment_status": status
        })
        
    return agents
