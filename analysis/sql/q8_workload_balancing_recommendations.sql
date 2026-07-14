-- Business Question 8: How can we balance workload better?
-- Rationale: Measure workload relative to active working hours and backlog sizes across functional teams.

select
    a.team,
    round(sum(c.tickets_assigned_that_day) / nullif(sum(c.scheduled_hours), 0), 3) as tickets_assigned_per_working_hour,
    round(avg(c.tickets_open_at_start_of_day), 2) as avg_daily_backlog
from marts.fact_agent_daily_capacity c
join marts.dim_agent a on c.agent_id = a.agent_id
group by a.team
order by tickets_assigned_per_working_hour desc;
