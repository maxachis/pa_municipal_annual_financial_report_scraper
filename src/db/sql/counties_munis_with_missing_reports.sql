/*
This query returns counties/municipalities that have missing reports for a given time frame.
 */

select
    c.name as "County",
    m.name as "Municipality",
    count(*) as "Count"
from
    counties c
    join municipalities m
         on m.county_id = c.id
    join annual_reports ar
         on ar.county_id = c.id and ar.municipality_id = m.id
    join scrape_info si
         on si.report_id = ar.id
where ar.year > 2019 -- Change this to <= change timeframe
and si.filename is not null
group by c.name, m.name
having count(*) < 4 and count(*) > 0 -- Change 4 to 5 for 2015-2019 timeframe
