-- Business Question 9: What root causes are hurting customer satisfaction?
-- Rationale: Map customer satisfaction averages against SLA failures, reopens, and escalation paths.

select
    round(avg(csat_score), 2) as overall_avg_csat,
    round(avg(case when sla_resolution_breached then csat_score else null end), 2) as breached_resolution_sla_avg_csat,
    round(avg(case when not sla_resolution_breached then csat_score else null end), 2) as met_resolution_sla_avg_csat,
    round(avg(case when reopened_count > 0 then csat_score else null end), 2) as reopened_tickets_avg_csat,
    round(avg(case when reopened_count = 0 then csat_score else null end), 2) as clean_tickets_avg_csat,
    round(avg(case when is_escalated then csat_score else null end), 2) as escalated_tickets_avg_csat,
    round(avg(case when not is_escalated then csat_score else null end), 2) as non_escalated_tickets_avg_csat
from marts.fact_ticket
where csat_score is not null;
