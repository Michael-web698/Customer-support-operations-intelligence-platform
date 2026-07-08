select
    ticket_id,
    customer_id,
    channel,
    category,
    priority,
    subject,
    description,
    created_at::timestamp as created_at,
    nullif(first_response_at, '')::timestamp as first_response_at,
    nullif(escalated_at, '')::timestamp as escalated_at,
    nullif(resolved_at, '')::timestamp as resolved_at,
    nullif(closed_at, '')::timestamp as closed_at,
    nullif(csat_score::text, '')::numeric::integer as csat_score,
    reopened_count::integer as reopened_count,
    current_status,
    assigned_agent_id as agent_id
from {{ source('raw', 'raw_tickets') }}
