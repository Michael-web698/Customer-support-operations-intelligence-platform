-- Business Question 10: How can leadership monitor support performance over time (trend + forecast)?
-- Rationale: Group operational trends by monthly periods to review volume growth, speed, SLA rates, and satisfaction.

select
    d.fiscal_period,
    count(f.ticket_id) as monthly_ticket_volume,
    round(avg(f.resolution_time_minutes) / 60.0, 2) as avg_resolution_hours,
    round(100.0 * sum(case when not f.sla_resolution_breached then 1 else 0 end) / count(f.ticket_id), 2) as resolution_sla_compliance_pct,
    round(avg(f.csat_score), 2) as avg_csat
from marts.fact_ticket f
join marts.dim_date d on f.created_date = d.date_day
group by d.fiscal_period
order by d.fiscal_period;
