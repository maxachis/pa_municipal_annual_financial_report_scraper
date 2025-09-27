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
            sum(
                    fed.report_total) as "FEDERAL 5-YEAR TOTAL"
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
            sum(
                    sta.report_total) as "STATE 5-YEAR TOTAL"
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
            sum(
                    loc.report_total) as "LOCAL 5-YEAR TOTAL"
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
    , tot_rev_five_year as (
        select
            ar.municipality_id,
            sum(
                    tr.total) as "TOTAL REVENUE 5-YEAR TOTAL"
        from
            annual_reports ar
            join total_revenue tr
                 on tr.report_id = ar.id
        where
            year <= 2019
        group by
            ar.municipality_id
        )
    , tab_3 as (
        select
            lmc.geo_id as "GEOID"
            , c.name as "COUNTY"
            , m.name as "MUNICIPALITY"
            , mc.class as "CLASS"
            , c.urban_rural as "URBAN/RURAL"
            , cmc.population as "POPULATION ESTIMATE"
            , Null as "POPULATION MARGIN"
            , fed."FEDERAL 5-YEAR TOTAL" as "FEDERAL GRANTS 5-YEAR TOTAL"
            , sta."STATE 5-YEAR TOTAL" as "STATE GRANTS 5-YEAR TOTAL"
            , loc."LOCAL 5-YEAR TOTAL" as "LOCAL GRANTS 5-YEAR TOTAL"
            , (
                fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" +
                loc."LOCAL 5-YEAR TOTAL") as "ALL GRANTS 5-YEAR TOTAL"
            , CASE
                  WHEN cmc.population = 0 THEN NULL
                  ELSE
                      fed."FEDERAL 5-YEAR TOTAL" / cmc.population END as "FEDERAL GRANTS 5-YR TOTAL PER CAPITA"
            , CASE
                  WHEN cmc.population = 0 THEN NULL
                  ELSE
                      sta."STATE 5-YEAR TOTAL" / cmc.population END as "STATE GRANTS 5-YR TOTAL PER CAPITA"
            , CASE
                  WHEN cmc.population = 0 THEN NULL
                  ELSE
                      loc."LOCAL 5-YEAR TOTAL" / cmc.population END as "LOCAL GRANTS 5-YR TOTAL PER CAPITA"
            , CASE
                  WHEN cmc.population = 0 THEN NULL
                  ELSE
                      (
                          fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" + loc."LOCAL 5-YEAR TOTAL") /
                      cmc.population END as "ALL GRANTS 5-YR TOTAL PER CAPITA"
            , rev."TOTAL REVENUE 5-YEAR TOTAL"
            , CASE
                  WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL
                  ELSE
                      fed."FEDERAL 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV FED GRANTS"
            , CASE
                  WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL
                  ELSE
                      sta."STATE 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV STATE GRANTS"
            , CASE
                  WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL
                  ELSE
                      loc."LOCAL 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV LOCAL GRANTS"
            , CASE
                  WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL
                  ELSE
                      (
                          fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" + loc."LOCAL 5-YEAR TOTAL") /
                      rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV ALL GRANTS"
        from
            counties c
            join municipalities m
                 on c.id = m.county_id
            join muni_classification mc
                 on m.id = mc.municipality_id
            join link_municipality_census lmc
                 on lmc.municipality_id = m.id
            join census_municipality_population cmc
                 on cmc.geo_id = lmc.geo_id and cmc.year = 2023
            join fed_five_year fed
                 on fed.municipality_id = m.id
            join sta_five_year sta
                 on sta.municipality_id = m.id
            join loc_five_year loc
                 on loc.municipality_id = m.id
            join tot_rev_five_year rev
                 on rev.municipality_id = m.id
        where
            not exists (
                select
                    1
                from
                    flag_invalid_municipalities im
                where
                    im.municipality_id = m.id
                )
        )
select distinct
    "County",
    "Municipality"
from tab_1
except
select distinct
    "COUNTY",
    "MUNICIPALITY"
from tab_3