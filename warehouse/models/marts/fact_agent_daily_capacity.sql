select
    agent_id,
    date as date_day,
    scheduled_hours,
    tickets_open_at_start_of_day,
    tickets_assigned_that_day
from {{ ref('stg_agent_daily_capacity') }}
