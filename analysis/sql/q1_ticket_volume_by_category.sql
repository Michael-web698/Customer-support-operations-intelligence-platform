-- Business Question 1: Which ticket categories are driving the most support volume?
-- Rationale: Identify high-volume categories to prioritize process automation or documentation.

select
    c.category_name,
    count(f.ticket_id) as ticket_count,
    round(100.0 * count(f.ticket_id) / sum(count(f.ticket_id)) over(), 2) as pct_of_total
from marts.fact_ticket f
join marts.dim_category c on f.category_key = c.category_key
group by c.category_name
order by ticket_count desc;
