/*
Get counties/munis with no reports
*/
select
    c.name as "County",
    m.name as "Municipality"
from
    counties c
    join municipalities m
         on m.county_id = c.id
where
    not exists (
        select
            1
        from
            annual_reports ar
            join scrape_info si
                 on si.report_id = ar.id and si.filename is not null
        where
            ar.municipality_id = m.id
        and ar.year >= 2020  -- Modify this to change the time frame
        )
