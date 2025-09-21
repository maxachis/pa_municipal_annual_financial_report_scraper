

GET_FIVE_YEAR_AVG_SCRIPT = """

with fed_five_year as (
    select
        ar.municipality_id,
        avg(fed.report_total) as "FEDERAL 5-YEAR AVERAGE"
        from federal_total_per_report fed
        join annual_reports ar on ar.id = fed.report_id
        where year {year_cond}
        group by municipality_id
    )
,sta_five_year as (
        select
            ar.municipality_id,
            avg(sta.report_total) as "STATE 5-YEAR AVERAGE"
        from state_total_per_report sta
             join annual_reports ar on ar.id = sta.report_id
        where year {year_cond}
        group by municipality_id
)
,loc_five_year as (
        select
            ar.municipality_id,
            avg(loc.report_total) as "LOCAL 5-YEAR AVERAGE"
        from local_total_per_report loc
             join annual_reports ar on ar.id = loc.report_id
        where year {year_cond}
        group by municipality_id
)


select
    c.name as "COUNTY",
    m.name as "MUNICIPALITY",
    mc.class as "CLASS",
    c.urban_rural as "URBAN/RURAL",
    fed."FEDERAL 5-YEAR AVERAGE" as " FEDERAL 5-YEAR AVERAGE",
    sta."STATE 5-YEAR AVERAGE",
    loc."LOCAL 5-YEAR AVERAGE",
    (fed."FEDERAL 5-YEAR AVERAGE" + sta."STATE 5-YEAR AVERAGE" + loc."LOCAL 5-YEAR AVERAGE") as "TOTAL 5-YEAR AVERAGE"

    from counties c
    join municipalities m on c.id = m.county_id
    join muni_classification mc on m.id = mc.municipality_id
    join fed_five_year fed on fed.municipality_id = m.id
    join sta_five_year sta on sta.municipality_id = m.id
    join loc_five_year loc on loc.municipality_id = m.id
order by c.name asc, m.name asc

"""