select
    event_id,
    ticket_id,
    event_type,
    event_timestamp,
    event_timestamp::date as event_date,
    from_agent_id,
    to_agent_id,
    from_status,
    to_status
from {{ ref('stg_ticket_events') }}
