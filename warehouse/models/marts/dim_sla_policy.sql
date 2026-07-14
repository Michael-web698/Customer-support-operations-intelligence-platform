with categories as (
    select 'Billing' as category_name union all
    select 'Technical' union all
    select 'Login/Access' union all
    select 'Product Feedback' union all
    select 'General'
),
priorities as (
    select 'Low' as priority, 1440 as target_response_minutes, 4320 as target_resolution_minutes union all
    select 'Medium', 480, 1440 union all
    select 'High', 120, 480 union all
    select 'Urgent', 30, 120
)
select
    md5(c.category_name || '_' || p.priority) as sla_policy_key,
    c.category_name,
    p.priority,
    p.target_response_minutes,
    p.target_resolution_minutes
from categories c
cross join priorities p
