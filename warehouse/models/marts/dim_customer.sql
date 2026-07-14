select
    customer_id,
    segment,
    region,
    signup_date,
    plan_tier
from {{ ref('stg_customers') }}
