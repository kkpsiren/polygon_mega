# Daily New Addresses on Polygon Overtime
# https://app.flipsidecrypto.com/velocity/queries/2124494c-5ce5-4639-94a1-777f713f46dd
QUERY = """with new_poly as (
  select from_address as address , min(block_timestamp)::date as min_date
  from flipside_prod_db.polygon.transactions
  group by address

)  
  select count(address) as new_address, min_date,
  	sum(new_address) over (order by min_date asc rows between unbounded preceding and current row) as cumulative_address  
  from new_poly group by min_date""" 

QUERY2 = """with new_poly_2020 as (
  select from_address as address , min(block_timestamp)::date as min_date, '2020' as type
  from flipside_prod_db.polygon.transactions
  group by address
    having min_date <= '2020-12-31' and min_date >= '2020-01-01'
)  , new_poly_2021 as (
  select from_address as address , min(block_timestamp)::date as min_date, '2021' as type
  from flipside_prod_db.polygon.transactions
  group by address
    having min_date <= '2021-12-31' and min_date >= '2021-01-01'
)  , new_poly_2022 as (
  select from_address as address , min(block_timestamp)::date as min_date, '2022' as type
  from flipside_prod_db.polygon.transactions
  group by address
    having min_date >= '2022-01-01' and min_date <= getdate()
)  
  select count(address)/365 as new_address, type
  from new_poly_2020 group by  type
	UNION
  select count(address)/365  as new_address,  type
  from new_poly_2021 group by  type
	UNION
  select count(address)/datediff(day, '2022-01-01', getdate()) as new_address,  type
  from new_poly_2022 group by  type"""
  
QUERY3 = """WITH
  active_users as (
  SELECT
  distinct from_address as active_user--,
  --max(block_timestamp) as last_transaction
  from flipside_prod_db.polygon.transactions
  where block_timestamp>=CURRENT_DATE-INTERVAL '3 MONTHS'
  group by 1
  ),
  active_users_n as (
  select count (distinct active_user) as active_users_doing_transactions from active_users
  ),
active_users_2 as (
  SELECT
  distinct to_address as active_receiver--,
  --max(block_timestamp) as last_transaction
  from flipside_prod_db.polygon.transactions --where to_address not in (select active_user from active_users)
  where block_timestamp>=CURRENT_DATE-INTERVAL '3 MONTHS'
  group by 1
),
  active_users_21 as (
  SELECT
  count(distinct active_receiver) as active_users_receiving_tokens--,
  --last_transaction
  from active_users_2 
  where active_receiver not in (select active_user from active_users)
)
select 
active_users_doing_transactions,
active_users_receiving_tokens,
active_users_doing_transactions+active_users_receiving_tokens as current_total_active_users
from active_users_n, active_users_21"""

QUERY4 = """-- How many addresses on the MATIC network are active? What’s the daily evolution of active addresses? Is the activeness related some how to the price?
-- Hint: Active address is an address that has done at least one transaction or has received at least once a token in the past 3 months.
WITH
  active_users_n as (
  SELECT
  trunc(block_timestamp,'day') as date,
  count(distinct from_address) as active_users
  from flipside_prod_db.polygon.transactions
  group by 1
  ),
active_users_2_n as (
  SELECT
  trunc(block_timestamp,'day') as date,
  count(distinct to_address) as active_users
  from flipside_prod_db.polygon.transactions
  group by 1
),
price as (
  SELECT
  trunc(hour,'day') as date,
  avg(price) as price
  from flipside_prod_db.ethereum_core.fact_hourly_token_prices
  where symbol='MATIC'
  GROUP BY 1
  order by 1 ASC
  )
SELECT
x.date,
x.active_users as users_doing_transactions, y.active_users as users_receiving_tokens,
price as matic_price
from active_users_n x, active_users_2_n y, price z where x.date=y.date and x.date=z.date 
order by 1 asc"""

QUERY5 = """with cs as (
  select 
  		BALANCE_DATE as date,
		sum(balance) as circulating_supply,
        Count(user_address) as holders
  from flipside_prod_db.ethereum.erc20_balances
  	where 
  		CONTRACT_ADDRESS = lower('0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0')
 	and USER_ADDRESS not in ('0x50d669f43b484166680ecc3670e4766cdb0945ce', '0xcbfe11b78c2e6cb25c6eda2c6ff46cd4755c8fca',
  							'0xb316fa9fa91700d7084d377bfdc81eb9f232f5ff', '0xccb04768f3abcf1af1e749085ef67d8ec7c5fdd2','0x5e3ef299fddf15eaa0432e6e66473ace8c13d908')
group by date 
  ),
price as (
  select 
  		date_trunc('day', HOUR) as date,
  		avg(PRICE) as matic_average_price
  from flipside_prod_db.ethereum.token_prices_hourly
  	where TOKEN_ADDRESS = lower('0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0')
  group by date
)
select 
  	cs.date,
	cs.circulating_supply * p.matic_average_price as Market_Cap,
	p.matic_average_price,
  	cs.circulating_supply,
    cs.holders
from cs join price p on cs.date = p.date
"""

QUERY6 = """WITH
polygon AS (
	SELECT
		DATE_TRUNC('day', hour) AS date,
		ROUND(AVG(txn)) AS avg_txn,
        AVG(fee) AS fees
	FROM (
		SELECT
			DATE_TRUNC('hour', block_timestamp) AS hour,
			COUNT(tx_id) AS txn,
            sum(fee) AS fee
		FROM
			flipside_prod_db.polygon.transactions
		WHERE
			block_timestamp::date >= '2021-09-01'
		GROUP BY
			hour
	)
	GROUP BY
		date
	ORDER BY
		date
)
SELECT
*   
FROM
	polygon
"""
