-- Business Question 2: Which issues create the highest escalation risk?
-- Rationale: Highlight categories with high escalation rates to assign senior staff or improve training.

select
    c.category_name,
    count(f.ticket_id) as total_tickets,
    sum(case when f.is_escalated then 1 else 0 end) as escalated_tickets,
    round(100.0 * sum(case when f.is_escalated then 1 else 0 end) / count(f.ticket_id), 2) as escalation_rate_pct
from marts.fact_ticket f
join marts.dim_category c on f.category_key = c.category_key
group by c.category_name
order by escalation_rate_pct desc;
