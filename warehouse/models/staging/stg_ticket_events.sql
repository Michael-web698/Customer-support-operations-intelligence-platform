select
    event_id,
    ticket_id,
    event_type,
    event_timestamp::timestamp as event_timestamp,
    nullif(from_agent_id::text, '')::numeric::integer as from_agent_id,
    nullif(to_agent_id::text, '')::numeric::integer as to_agent_id,
    from_status,
    to_status
from {{ source('raw', 'raw_ticket_events') }}
