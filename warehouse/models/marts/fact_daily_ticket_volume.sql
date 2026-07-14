select
    created_at::date as date_day,
    category as category_name,
    count(*) as ticket_count
from {{ ref('stg_tickets') }}
group by 1, 2
order by 1 asc, 2 asc
