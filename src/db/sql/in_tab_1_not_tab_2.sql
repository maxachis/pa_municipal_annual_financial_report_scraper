/*
 Gets all values in tab 1 but not tab 2
 for the 2015-2019 time frame
 */
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
        where
            not exists(
                select
                    1
                from
                    flag_invalid_municipalities im
                where
                    im.municipality_id = m.id
                )
        )
    , tab_1 as (
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
            join total_revenue tr
                 on tr.report_id = ar.id
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
            ar.year <= 2019


        )
    , fed_five_year as (
        select
            ar.municipality_id,
            avg(fed.report_total) as "FEDERAL 5-YEAR AVERAGE"
        from
            federal_total_per_report fed
            join annual_reports ar
                 on ar.id = fed.report_id
        where
            year <= 2019
        group by
            municipality_id
        having
            count(*) >= 5
        )
    , sta_five_year as (
        select
            ar.municipality_id,
            avg(sta.report_total) as "STATE 5-YEAR AVERAGE"
        from
            state_total_per_report sta
            join annual_reports ar
                 on ar.id = sta.report_id
        where
            year <= 2019
        group by
            municipality_id
        having
            count(*) >= 5
        )
    , loc_five_year as (
        select
            ar.municipality_id,
            avg(loc.report_total) as "LOCAL 5-YEAR AVERAGE"
        from
            local_total_per_report loc
            join annual_reports ar
                 on ar.id = loc.report_id
        where
            year <= 2019
        group by
            municipality_id
        having
            count(*) >= 5
        )
    , tab_2 as (
        select
            c.name as "COUNTY",
            m.name as "MUNICIPALITY",
            mc.class as "CLASS",
            c.urban_rural as "URBAN/RURAL",
            fed."FEDERAL 5-YEAR AVERAGE" as " FEDERAL 5-YEAR AVERAGE",
            sta."STATE 5-YEAR AVERAGE",
            loc."LOCAL 5-YEAR AVERAGE",
            (fed."FEDERAL 5-YEAR AVERAGE" + sta."STATE 5-YEAR AVERAGE" +
             loc."LOCAL 5-YEAR AVERAGE") as "TOTAL 5-YEAR AVERAGE"

        from
            counties c
            join municipalities m
                 on c.id = m.county_id
            join muni_classification mc
                 on m.id = mc.municipality_id
            join fed_five_year fed
                 on fed.municipality_id = m.id
            join sta_five_year sta
                 on sta.municipality_id = m.id
            join loc_five_year loc
                 on loc.municipality_id = m.id
        where
            not exists(
                select
                    1
                from
                    flag_invalid_municipalities im
                where
                    im.municipality_id = m.id
                )
        order by
            c.name asc,
            m.name asc


        )
select distinct
    "County",
    "Municipality"
from tab_1
except
select distinct
    "COUNTY",
    "MUNICIPALITY"
from tab_2
