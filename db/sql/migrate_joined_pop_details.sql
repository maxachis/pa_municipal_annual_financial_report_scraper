INSERT INTO joined_pop_details_v2 (
   geo_id,
   class_,
   pop_estimate,
   pop_margin,
   location_type,
   county_id,
   municipality_id
)
SELECT
    jpd.geo_id,
    jpd.class_,
    jpd.pop_estimate,
    jpd.pop_margin,
    jpd.urban_rural::location_type,
    c.id,
    m.id
FROM joined_pop_details jpd
JOIN counties c ON c.name = jpd.county
JOIN municipalities m ON m.name = jpd.municipality