-- Business Question 7: Which agents are handling the most escalations?
-- Rationale: Identify escalation bottlenecks or key resolving specialists.

select
    a.agent_name,
    a.team,
    a.seniority_level,
    count(f.ticket_id) as total_tickets_handled,
    sum(case when f.is_escalated then 1 else 0 end) as escalated_tickets_handled,
    round(100.0 * sum(case when f.is_escalated then 1 else 0 end) / count(f.ticket_id), 2) as escalation_handling_pct
from marts.fact_ticket f
join marts.dim_agent a on f.agent_id = a.agent_id
group by a.agent_id, a.agent_name, a.team, a.seniority_level
order by escalated_tickets_handled desc;
