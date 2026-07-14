select
    t.ticket_id,
    t.customer_id,
    t.agent_id,
    md5(t.category) as category_key,
    md5(t.category || '_' || t.priority) as sla_policy_key,
    md5(t.channel) as channel_key,
    -- Date keys linking to dim_date
    t.created_at::date as created_date,
    t.resolved_at::date as resolved_date,
    t.closed_at::date as closed_date,
    -- Timestamps
    t.created_at,
    t.first_response_at,
    t.escalated_at,
    t.resolved_at,
    t.closed_at,
    -- Metadata
    t.priority,
    t.subject,
    t.description,
    -- Operational measures
    t.response_time_minutes,
    t.resolution_time_minutes,
    t.reopened_count,
    t.csat_score,
    t.sla_response_breached,
    t.sla_resolution_breached,
    t.is_escalated
from {{ ref('int_ticket_sla') }} t
