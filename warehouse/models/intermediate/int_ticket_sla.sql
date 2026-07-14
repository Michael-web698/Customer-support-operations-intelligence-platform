select
    t.ticket_id,
    t.customer_id,
    t.channel,
    t.category,
    t.priority,
    t.subject,
    t.description,
    t.created_at,
    t.first_response_at,
    t.escalated_at,
    t.resolved_at,
    t.closed_at,
    t.csat_score,
    t.reopened_count,
    t.current_status,
    t.agent_id,
    -- SLA Policy targets
    p.target_response_minutes,
    p.target_resolution_minutes,
    -- Calculated response and resolution durations in minutes
    extract(epoch from (t.first_response_at - t.created_at)) / 60 as response_time_minutes,
    extract(epoch from (t.resolved_at - t.created_at)) / 60 as resolution_time_minutes,
    -- SLA Breach Flags
    case
        when t.first_response_at is not null and (extract(epoch from (t.first_response_at - t.created_at)) / 60) > p.target_response_minutes then true
        else false
    end as sla_response_breached,
    case
        when t.resolved_at is not null and (extract(epoch from (t.resolved_at - t.created_at)) / 60) > p.target_resolution_minutes then true
        else false
    end as sla_resolution_breached,
    -- Other operational flags
    case when t.escalated_at is not null then true else false end as is_escalated
from {{ ref('stg_tickets') }} t
left join {{ ref('dim_sla_policy') }} p
    on t.category = p.category_name
    and t.priority = p.priority
