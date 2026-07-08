# ==============================================================================
# Customer Support Operations Intelligence Platform - Ticket & Event Generator
# ==============================================================================

import random
from datetime import datetime, timedelta
from data_generator.generators.text_templates import generate_text

CHANNELS = ["Email", "Chat", "Phone", "Social"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
PRIORITY_WEIGHTS = [0.50, 0.30, 0.15, 0.05]

SLA_POLICIES = {
    # priority: (response_target_min, resolution_target_min)
    "Low": (1440, 4320),       # 24h response, 72h resolution
    "Medium": (480, 1440),     # 8h response, 24h resolution
    "High": (120, 480),        # 2h response, 8h resolution
    "Urgent": (30, 120)        # 30m response, 2h resolution
}

def generate_tickets_and_events(customers, agents, start_date, end_date, config):
    """
    Simulates ticket lifecycle and events over the time range, applying correlations from config.
    """
    tickets = []
    events = []
    capacity_records = []
    
    current_event_id = 1
    current_ticket_id = 1
    
    # Track open tickets per agent
    # agent_id -> list of active ticket_ids
    active_tickets = {agent["agent_id"]: [] for agent in agents}
    
    # Track daily assignments to calculate daily capacity stats
    # agent_id -> count
    daily_assignments = {agent["agent_id"]: 0 for agent in agents}
    
    # Helper to pick working agents for a given day
    # We assign agents to a fixed 5-day work week based on their ID to simulate off-days
    def get_working_agents_for_date(date_obj):
        day_of_week = date_obj.weekday()
        working = []
        for agent in agents:
            # Simple schedule: agent works if (agent_id + day_of_week) % 7 < 5
            if (agent["agent_id"] + day_of_week) % 7 < 5:
                working.append(agent)
        return working

    # Initialize calendar loop
    date_cursor = start_date
    while date_cursor <= end_date:
        working_agents = get_working_agents_for_date(date_cursor)
        working_agent_ids = [a["agent_id"] for a in working_agents]
        
        # Calculate overall system load to check for overload state
        # load_ratio = active_tickets / total_capacity
        total_active = sum(len(active_tickets[a_id]) for a_id in active_tickets)
        total_capacity = sum(config["agent_seniority"][a["seniority_level"]]["capacity_limit"] for a in working_agents)
        system_load_ratio = total_active / max(total_capacity, 1)
        is_overloaded = system_load_ratio > config["overload"]["threshold_ratio"]
        
        # Record agent capacity at the start of the day
        for agent in agents:
            a_id = agent["agent_id"]
            is_working = a_id in working_agent_ids
            scheduled_hours = 8.0 if is_working else 0.0
            
            capacity_records.append({
                "agent_id": a_id,
                "date": date_cursor.strftime("%Y-%m-%d"),
                "scheduled_hours": scheduled_hours,
                "tickets_open_at_start_of_day": len(active_tickets[a_id]),
                "tickets_assigned_that_day": 0 # Will be updated at end of day
            })
            
        daily_assignments = {agent["agent_id"]: 0 for agent in agents}
        
        # Determine ticket volume for today
        day_of_week = date_cursor.weekday()
        base_volume = int(config["seasonality"]["weekly_trend"][day_of_week] * 80) # Base 80 tickets/day
        
        # Post-holiday spike simulation (e.g. Day after Christmas, Thanksgiving, New Years)
        # Check if today is e.g. July 5, Jan 2, Nov 27
        is_post_holiday = (date_cursor.month == 7 and date_cursor.day == 5) or \
                          (date_cursor.month == 1 and date_cursor.day == 2) or \
                          (date_cursor.month == 11 and date_cursor.day == 27)
        if is_post_holiday:
            base_volume = int(base_volume * config["seasonality"]["post_holiday_spike_multiplier"])
            
        # Add random noise
        daily_volume = int(base_volume * random.uniform(0.85, 1.15))
        
        # Generate tickets for today
        for _ in range(daily_volume):
            # Select Customer (signed up on or before today)
            available_customers = [c for c in customers if datetime.strptime(c["signup_date"], "%Y-%m-%d") <= datetime.combine(date_cursor, datetime.min.time())]
            if not available_customers:
                available_customers = customers # Fallback
            customer = random.choice(available_customers)
            
            # Select Category based on weights
            cats = list(config["categories"].keys())
            cat_weights = [config["categories"][c]["volume_weight"] for c in cats]
            category = random.choices(cats, weights=cat_weights)[0]
            
            # Select Priority
            priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
            channel = random.choice(CHANNELS)
            
            # Pick a sentiment for customer text
            sentiment = random.choices(["Positive", "Neutral", "Negative"], weights=[0.15, 0.60, 0.25])[0]
            subject, description = generate_text(category, sentiment)
            
            # Ticket creation timestamp (distributed throughout the working day 8am-8pm)
            hour = random.randint(8, 20)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            created_time = datetime.combine(date_cursor, datetime.min.time()) + timedelta(hours=hour, minutes=minute, seconds=second)
            
            # Pick assigned agent from working agents with least active load
            if working_agents:
                # Prioritize agents on relevant teams, else least loaded working agent
                # For simplicity, assign to the working agent with the lowest active load
                assigned_agent = min(working_agents, key=lambda a: len(active_tickets[a["agent_id"]]))
                assigned_agent_id = assigned_agent["agent_id"]
            else:
                # If no one working (rare), assign to a random agent
                assigned_agent = random.choice(agents)
                assigned_agent_id = assigned_agent["agent_id"]
                
            active_tickets[assigned_agent_id].append(current_ticket_id)
            daily_assignments[assigned_agent_id] += 1
            
            # Add creation and assignment events
            events.append({
                "event_id": current_event_id,
                "ticket_id": current_ticket_id,
                "event_type": "created",
                "event_timestamp": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "from_agent_id": None,
                "to_agent_id": None,
                "from_status": None,
                "to_status": "Open"
            })
            current_event_id += 1
            
            events.append({
                "event_id": current_event_id,
                "ticket_id": current_ticket_id,
                "event_type": "assigned",
                "event_timestamp": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "from_agent_id": None,
                "to_agent_id": assigned_agent_id,
                "from_status": "Open",
                "to_status": "Open"
            })
            current_event_id += 1
            
            # --- Lifecycle Duration Calculations ---
            
            # 1. First Response Time (FRT)
            # Base target response time in minutes
            base_response_target = SLA_POLICIES[priority][0]
            
            # Actual FRT calculation
            segment_multiplier = config["customer_segments"][customer["segment"]]["routing_speed_multiplier"]
            overload_mult = config["overload"]["first_response_delay_multiplier"] if is_overloaded else 1.0
            
            # Random delay based on priority
            if priority == "Urgent":
                frt_minutes = random.randint(5, 45)
            elif priority == "High":
                frt_minutes = random.randint(15, 180)
            elif priority == "Medium":
                frt_minutes = random.randint(60, 600)
            else:
                frt_minutes = random.randint(120, 1440)
                
            # Apply multipliers
            actual_frt_minutes = int(frt_minutes * segment_multiplier * overload_mult)
            first_response_at = created_time + timedelta(minutes=actual_frt_minutes)
            
            # Add responded event
            events.append({
                "event_id": current_event_id,
                "ticket_id": current_ticket_id,
                "event_type": "responded",
                "event_timestamp": first_response_at.strftime("%Y-%m-%d %H:%M:%S"),
                "from_agent_id": assigned_agent_id,
                "to_agent_id": assigned_agent_id,
                "from_status": "Open",
                "to_status": "Pending"
            })
            current_event_id += 1
            
            # 2. Escalation Logic
            escalated_at = None
            base_escalation_prob = config["categories"][category]["base_escalation_prob"]
            # Junior agents escalate more frequently
            agent_seniority_level = assigned_agent["seniority_level"]
            if agent_seniority_level == "Junior":
                base_escalation_prob *= 1.8
            elif agent_seniority_level == "Senior":
                base_escalation_prob *= 0.5
                
            # High priority escalates slightly more
            if priority in ["High", "Urgent"]:
                base_escalation_prob += 0.05
                
            will_escalate = random.random() < base_escalation_prob
            final_agent_id = assigned_agent_id
            
            if will_escalate:
                # Escalates shortly after response
                escalated_delay = random.randint(10, 120)
                escalated_at = first_response_at + timedelta(minutes=escalated_delay)
                
                # Reassigned to a senior agent or mid-level agent
                eligible_escalation_agents = [a for a in agents if a["seniority_level"] in ["Mid", "Senior"] and a["agent_id"] != assigned_agent_id]
                if not eligible_escalation_agents:
                    eligible_escalation_agents = agents # Fallback
                escalation_agent = random.choice(eligible_escalation_agents)
                final_agent_id = escalation_agent["agent_id"]
                
                # Add escalated event
                events.append({
                    "event_id": current_event_id,
                    "ticket_id": current_ticket_id,
                    "event_type": "escalated",
                    "event_timestamp": escalated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "from_agent_id": assigned_agent_id,
                    "to_agent_id": final_agent_id,
                    "from_status": "Pending",
                    "to_status": "Open"
                })
                current_event_id += 1
                
                # Update active tickets trackers
                if current_ticket_id in active_tickets[assigned_agent_id]:
                    active_tickets[assigned_agent_id].remove(current_ticket_id)
                active_tickets[final_agent_id].append(current_ticket_id)
                
            # 3. Resolution Logic
            # Base complexity in hours
            base_complexity_hours = config["categories"][category]["base_complexity"] * 8 # 8h scale
            agent_level = agents[final_agent_id - 1]["seniority_level"]
            agent_mult = config["agent_seniority"][agent_level]["resolution_speed_multiplier"]
            overload_mult = config["overload"]["resolution_delay_multiplier"] if is_overloaded else 1.0
            
            # Resolve duration in minutes
            resolve_minutes = int(base_complexity_hours * 60 * agent_mult * overload_mult * random.uniform(0.7, 1.3))
            
            # Standard SLA resolution targets
            base_resolution_target = SLA_POLICIES[priority][1]
            
            # Boost SLA breach chance under overload
            if is_overloaded and random.random() < config["overload"]["sla_breach_probability_boost"]:
                resolve_minutes = max(resolve_minutes, base_resolution_target + random.randint(10, 500))
                
            anchor_time = escalated_at if escalated_at else first_response_at
            resolved_at = anchor_time + timedelta(minutes=resolve_minutes)
            
            # Add resolved event
            events.append({
                "event_id": current_event_id,
                "ticket_id": current_ticket_id,
                "event_type": "resolved",
                "event_timestamp": resolved_at.strftime("%Y-%m-%d %H:%M:%S"),
                "from_agent_id": final_agent_id,
                "to_agent_id": final_agent_id,
                "from_status": "Open" if will_escalate else "Pending",
                "to_status": "Resolved"
            })
            current_event_id += 1
            
            # 4. Reopen Logic
            # Probability of reopen based on agent seniority and customer expectations
            base_reopen_prob = 0.05 # 5% base
            reopen_mult = config["agent_seniority"][agent_level]["reopen_probability_multiplier"]
            reopen_prob = base_reopen_prob * reopen_mult
            
            # Pro/Enterprise customers reopen slightly more to get better service
            if customer["segment"] == "Enterprise":
                reopen_prob += 0.04
            elif customer["segment"] == "Pro":
                reopen_prob += 0.02
                
            will_reopen = random.random() < reopen_prob
            reopened_count = 0
            
            if will_reopen:
                reopened_count = 1
                # Reopens 1-6 hours after resolution
                reopen_delay = random.randint(60, 360)
                reopened_at = resolved_at + timedelta(minutes=reopen_delay)
                
                # Add reopened event
                events.append({
                    "event_id": current_event_id,
                    "ticket_id": current_ticket_id,
                    "event_type": "reopened",
                    "event_timestamp": reopened_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "from_agent_id": final_agent_id,
                    "to_agent_id": final_agent_id,
                    "from_status": "Resolved",
                    "to_status": "Open"
                })
                current_event_id += 1
                
                # Re-resolve after some time
                re_resolve_delay = random.randint(30, 240)
                resolved_at = reopened_at + timedelta(minutes=re_resolve_delay)
                
                # Add second resolved event
                events.append({
                    "event_id": current_event_id,
                    "ticket_id": current_ticket_id,
                    "event_type": "resolved",
                    "event_timestamp": resolved_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "from_agent_id": final_agent_id,
                    "to_agent_id": final_agent_id,
                    "from_status": "Open",
                    "to_status": "Resolved"
                })
                current_event_id += 1
                
            # 5. Close Logic
            # Auto-close 24-48 hours after resolution
            close_delay_hours = random.randint(24, 48)
            closed_at = resolved_at + timedelta(hours=close_delay_hours)
            
            # Add closed event
            events.append({
                "event_id": current_event_id,
                "ticket_id": current_ticket_id,
                "event_type": "closed",
                "event_timestamp": closed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "from_agent_id": final_agent_id,
                "to_agent_id": final_agent_id,
                "from_status": "Resolved",
                "to_status": "Closed"
            })
            current_event_id += 1
            
            # Remove from active tickets once resolved/closed
            if current_ticket_id in active_tickets[final_agent_id]:
                active_tickets[final_agent_id].remove(current_ticket_id)
                
            # 6. CSAT calculation
            # Only calculated for closed tickets
            # Standard CSAT response rate (e.g. 35%)
            has_csat = random.random() < 0.35
            csat_score = None
            if has_csat:
                csat_val = config["csat"]["base_score"]
                
                # Penalties
                csat_val += reopened_count * config["csat"]["reopen_penalty"]
                if escalated_at:
                    csat_val += config["csat"]["escalation_penalty"]
                    
                # Resolution delay penalty
                total_resolution_hours = (resolved_at - created_time).total_seconds() / 3600
                csat_val += total_resolution_hours * config["csat"]["resolution_delay_penalty_per_hour"]
                
                # SLA checks
                sla_response_breached = actual_frt_minutes > base_response_target
                sla_resolution_breached = (resolved_at - created_time).total_seconds() / 60 > base_resolution_target
                if sla_response_breached or sla_resolution_breached:
                    csat_val += config["csat"]["sla_breach_penalty"]
                    
                # Overload effects
                if is_overloaded:
                    csat_val *= config["overload"]["csat_degradation_multiplier"]
                    
                # Customer segment offsets (expectations)
                csat_val += config["customer_segments"][customer["segment"]]["base_csat_offset"]
                
                # Bound CSAT to 1.0 - 5.0 and round to nearest integer
                csat_score = int(round(clip(csat_val, 1.0, 5.0)))
                
            # Compile final ticket details
            tickets.append({
                "ticket_id": current_ticket_id,
                "customer_id": customer["customer_id"],
                "channel": channel,
                "category": category,
                "priority": priority,
                "subject": subject,
                "description": description,
                "created_at": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "first_response_at": first_response_at.strftime("%Y-%m-%d %H:%M:%S"),
                "escalated_at": escalated_at.strftime("%Y-%m-%d %H:%M:%S") if escalated_at else "",
                "resolved_at": resolved_at.strftime("%Y-%m-%d %H:%M:%S"),
                "closed_at": closed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "csat_score": csat_score if csat_score is not None else "",
                "reopened_count": reopened_count,
                "current_status": "Closed", # All generated tickets are closed in the past history
                "assigned_agent_id": final_agent_id
            })
            
            current_ticket_id += 1
            
        # Update daily capacity assignments count
        for record in capacity_records:
            if record["date"] == date_cursor.strftime("%Y-%m-%d"):
                record["tickets_assigned_that_day"] = daily_assignments[record["agent_id"]]
                
        date_cursor += timedelta(days=1)
        
    return tickets, events, capacity_records

def clip(val, min_val, max_val):
    return max(min(val, max_val), min_val)
