-- Business Question 3: Which agents are overloaded, and who has capacity?
-- Rationale: Measure active backlog and daily assignment counts per agent on working days.

select
    a.agent_name,
    a.team,
    a.seniority_level,
    round(avg(c.scheduled_hours), 2) as avg_scheduled_hours,
    round(avg(c.tickets_open_at_start_of_day), 2) as avg_open_tickets_backlog,
    round(avg(c.tickets_assigned_that_day), 2) as avg_daily_assignments
from marts.fact_agent_daily_capacity c
join marts.dim_agent a on c.agent_id = a.agent_id
where c.scheduled_hours > 0 -- Focus only on working shifts
group by a.agent_id, a.agent_name, a.team, a.seniority_level
order by avg_open_tickets_backlog desc;
