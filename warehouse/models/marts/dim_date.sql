with dates as (
    select
        datum::date as date_day
    from generate_series(
        '2025-01-01'::date,
        '2027-12-31'::date,
        '1 day'::interval
    ) as datum
)
select
    date_day,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day,
    extract(dow from date_day) as day_of_week, -- 0 = Sunday, 6 = Saturday
    trim(to_char(date_day, 'Day')) as day_name,
    trim(to_char(date_day, 'Month')) as month_name,
    case when extract(dow from date_day) in (0, 6) then true else false end as is_weekend,
    extract(quarter from date_day) as quarter,
    to_char(date_day, 'YYYY-"P"MM') as fiscal_period
from dates
order by date_day asc
