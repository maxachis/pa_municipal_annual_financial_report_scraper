GET_BY_YEAR_MUNI_SCRIPT = """

with
    new_counties as (
        select
            id,
            name
        from
            counties
        )
    , new_municipalities as (
        select
            m.*
        from
            municipalities m
            join counties c
                 on c.id = m.county_id
        )
select
    c.name as "County",
    m.name as "Municipality",
    ar.year as "Year",
    tr.total as "Total revenue",
    fed.report_total as "Federal Grants",
    sta.report_total as "State Grants",
    loc.report_total as "Local Grants",
    (fed.report_total + sta.report_total + loc.report_total) as "All grants"
from
    annual_reports ar
    join total_revenue tr on tr.report_id = ar.id
    join new_counties c
         on c.id = ar.county_id
    join new_municipalities m
         on m.county_id = c.id and m.id = ar.municipality_id
    join federal_total_per_report fed
         on fed.report_id = ar.id
    join state_total_per_report sta
         on sta.report_id = ar.id
    join local_total_per_report loc
         on loc.report_id = ar.id

where
    ar.year {year_cond}



"""