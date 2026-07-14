select
    agent_id,
    agent_name,
    team,
    seniority_level,
    hire_date,
    shift,
    employment_status
from {{ ref('stg_agents') }}
