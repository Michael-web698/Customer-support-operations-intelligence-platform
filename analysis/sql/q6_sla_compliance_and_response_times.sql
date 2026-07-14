-- Business Question 6: How can response times and SLA compliance be improved?
-- Rationale: Find response averages and breach metrics by category and priority to pinpoint weak spots.

select
    c.category_name,
    f.priority,
    count(f.ticket_id) as total_tickets,
    round(avg(f.response_time_minutes), 2) as avg_response_minutes,
    round(100.0 * sum(case when f.sla_response_breached then 1 else 0 end) / count(f.ticket_id), 2) as response_sla_breach_pct,
    round(100.0 * sum(case when f.sla_resolution_breached then 1 else 0 end) / count(f.ticket_id), 2) as resolution_sla_breach_pct
from marts.fact_ticket f
join marts.dim_category c on f.category_key = c.category_key
group by c.category_name, f.priority
order by c.category_name, f.priority;
