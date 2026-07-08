select
    agent_id,
    date::date as date,
    scheduled_hours::numeric as scheduled_hours,
    tickets_open_at_start_of_day::integer as tickets_open_at_start_of_day,
    tickets_assigned_that_day::integer as tickets_assigned_that_day
from {{ source('raw', 'raw_agent_daily_capacity') }}
