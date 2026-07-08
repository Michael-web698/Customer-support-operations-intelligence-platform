select
    customer_id,
    segment,
    region,
    signup_date::date as signup_date,
    plan_tier
from {{ source('raw', 'raw_customers') }}
