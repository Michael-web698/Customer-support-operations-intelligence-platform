with categories as (
    select 'Billing' as category_name, 'Billing/Finance' as parent_category, 1.0 as default_complexity_score union all
    select 'Technical', 'Tech Support', 2.0 union all
    select 'Login/Access', 'Account Admin', 0.5 union all
    select 'Product Feedback', 'Product Management', 0.8 union all
    select 'General', 'General Info', 0.7
)
select
    md5(category_name) as category_key,
    category_name,
    parent_category,
    default_complexity_score
from categories
