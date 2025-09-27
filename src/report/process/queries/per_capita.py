


GET_PER_CAPITA_SCRIPT = """
with fed_five_year as (
    select
        ar.municipality_id,
        sum(fed.report_total) as "FEDERAL 5-YEAR TOTAL"
        from federal_total_per_report fed
        join annual_reports ar on ar.id = fed.report_id
        where year {year_cond}
        group by municipality_id
        {having_clause} 
)
,sta_five_year as (
        select
            ar.municipality_id,
            sum(sta.report_total) as "STATE 5-YEAR TOTAL"
        from state_total_per_report sta
             join annual_reports ar on ar.id = sta.report_id
        where year {year_cond}
        group by municipality_id
        {having_clause}
)
,loc_five_year as (
        select
            ar.municipality_id,
            sum(loc.report_total) as "LOCAL 5-YEAR TOTAL"
        from local_total_per_report loc
             join annual_reports ar on ar.id = loc.report_id
        where year {year_cond}
        group by municipality_id
        {having_clause}
)
, tot_rev_five_year as (
    select
        ar.municipality_id,
        sum(tr.total) as "TOTAL REVENUE 5-YEAR TOTAL"
    from annual_reports ar
    join total_revenue tr on tr.report_id = ar.id
    where year {year_cond}
    group by ar.municipality_id
)


select
    lmc.geo_id as "GEOID",
    c.name as "COUNTY",
    m.name as "MUNICIPALITY",
    mc.class as "CLASS",
    c.urban_rural as "URBAN/RURAL",
    cmc.population as "POPULATION ESTIMATE",
    Null as "POPULATION MARGIN",
    fed."FEDERAL 5-YEAR TOTAL" as "FEDERAL GRANTS 5-YEAR TOTAL",
    sta."STATE 5-YEAR TOTAL" as "STATE GRANTS 5-YEAR TOTAL",
    loc."LOCAL 5-YEAR TOTAL" as "LOCAL GRANTS 5-YEAR TOTAL",
    (fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" + loc."LOCAL 5-YEAR TOTAL") as "ALL GRANTS 5-YEAR TOTAL",
    CASE WHEN cmc.population = 0 THEN NULL ELSE
        fed."FEDERAL 5-YEAR TOTAL" / cmc.population END as "FEDERAL GRANTS 5-YR TOTAL PER CAPITA",
    CASE WHEN cmc.population = 0 THEN NULL ELSE
        sta."STATE 5-YEAR TOTAL" / cmc.population END as "STATE GRANTS 5-YR TOTAL PER CAPITA",
    CASE WHEN cmc.population = 0 THEN NULL ELSE
        loc."LOCAL 5-YEAR TOTAL" / cmc.population END as "LOCAL GRANTS 5-YR TOTAL PER CAPITA",
    CASE WHEN cmc.population = 0 THEN NULL ELSE
        (fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" + loc."LOCAL 5-YEAR TOTAL") / cmc.population END as "ALL GRANTS 5-YR TOTAL PER CAPITA",
    rev."TOTAL REVENUE 5-YEAR TOTAL",
    CASE WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL ELSE
        fed."FEDERAL 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV FED GRANTS",
    CASE WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL ELSE
        sta."STATE 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV STATE GRANTS",
    CASE WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL ELSE
        loc."LOCAL 5-YEAR TOTAL" / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV LOCAL GRANTS",
    CASE WHEN rev."TOTAL REVENUE 5-YEAR TOTAL" = 0 THEN NULL ELSE
        (fed."FEDERAL 5-YEAR TOTAL" + sta."STATE 5-YEAR TOTAL" + loc."LOCAL 5-YEAR TOTAL") / rev."TOTAL REVENUE 5-YEAR TOTAL" END as "% REV ALL GRANTS"
    from counties c
    join municipalities m on c.id = m.county_id
    join muni_classification mc on m.id = mc.municipality_id
    join link_municipality_census lmc on lmc.municipality_id = m.id
    join census_municipality_population cmc on cmc.geo_id = lmc.geo_id and cmc.year = {year}
    join fed_five_year fed on fed.municipality_id = m.id
    join sta_five_year sta on sta.municipality_id = m.id
    join loc_five_year loc on loc.municipality_id = m.id
    join tot_rev_five_year rev on rev.municipality_id = m.id
        where not exists(select 1 \
                     from flag_invalid_municipalities im \
                     where im.municipality_id = m.id)
"""
