with channels as (
    select 'Email' as channel_name union all
    select 'Chat' union all
    select 'Phone' union all
    select 'Social'
)
select
    md5(channel_name) as channel_key,
    channel_name
from channels
