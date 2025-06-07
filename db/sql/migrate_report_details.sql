INSERT INTO
    report_details (report_id, total)
SELECT
    ar.report_id,
    afrd.total
    FROM
        annual_reports ar
        JOIN COUNTIES c
            ON c.id = ar.county_id
        JOIN MUNICIPALITIES m
            ON m.id = ar.municipality_id
        JOIN annual_financial_report_details afrd
            ON
            afrd.county = c.name
                AND afrd.municipality = m.name
                AND afrd.year = ar.year
