select
    agent_id,
    name as agent_name,
    team,
    seniority_level,
    hire_date::date as hire_date,
    shift,
    employment_status
from {{ source('raw', 'raw_agents') }}
