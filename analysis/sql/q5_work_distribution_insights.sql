-- Business Question 5: How should work be distributed among agents?
-- Rationale: Assess workloads, resolution times, and quality (reopen rates) across agent seniority groups.

select
    a.seniority_level,
    count(f.ticket_id) as total_tickets_handled,
    round(avg(f.resolution_time_minutes) / 60.0, 2) as avg_resolution_hours,
    round(100.0 * sum(case when f.reopened_count > 0 then 1 else 0 end) / count(f.ticket_id), 2) as reopen_rate_pct
from marts.fact_ticket f
join marts.dim_agent a on f.agent_id = a.agent_id
group by a.seniority_level
order by total_tickets_handled desc;
