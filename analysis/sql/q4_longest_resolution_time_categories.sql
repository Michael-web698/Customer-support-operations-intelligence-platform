-- Business Question 4: Which categories take the longest to resolve?
-- Rationale: Identify bottlenecks in resolution times to streamline root causes.

select
    c.category_name,
    count(f.ticket_id) as resolved_tickets,
    round(avg(f.resolution_time_minutes) / 60.0, 2) as avg_resolution_hours,
    round((percentile_cont(0.5) within group (order by f.resolution_time_minutes) / 60.0)::numeric, 2) as median_resolution_hours
from marts.fact_ticket f
join marts.dim_category c on f.category_key = c.category_key
where f.resolved_at is not null
group by c.category_name
order by avg_resolution_hours desc;
