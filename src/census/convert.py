from src.census.api.model import CensusData
from src.census.extract import extract_county_name, extract_municipality_name
from src.db.models.sqlalchemy.impl.census.county import CensusCounty
from src.db.models.sqlalchemy.impl.census.municipality import CensusMunicipality
from src.db.models.sqlalchemy.impl.census.municipality_population import CensusMunicipalityPopulation


def convert_census_data_to_census_county(
    census_data: list[CensusData]
) -> list[CensusCounty]:
    id_to_county: dict[int, CensusCounty] = {}
    for data in census_data:
        if data.county_id not in id_to_county:
            county_name: str = extract_county_name(data.name)
            id_to_county[data.county_id] = CensusCounty(
                id=data.county_id,
                name=county_name,
            )

    return list(id_to_county.values())

def convert_census_data_to_census_municipality(
    census_data: list[CensusData]
) -> list[CensusMunicipality]:
    census_municipalities: list[CensusMunicipality] = []
    for data in census_data:
        municipality_name: str = extract_municipality_name(data.name)
        municipality = CensusMunicipality(
            census_county_id=data.county_id,
            name=municipality_name,
            geo_id=data.geo_id,
        )
        census_municipalities.append(municipality)
    return census_municipalities

def convert_census_data_to_census_municipality_pop(
    census_data: list[CensusData],
    year: int,
) -> list[CensusMunicipalityPopulation]:
    census_municipality_pops: list[CensusMunicipalityPopulation] = []
    for data in census_data:
        municipality_pop = CensusMunicipalityPopulation(
            geo_id=data.geo_id,
            year=year,
            population=data.population,
        )
        census_municipality_pops.append(municipality_pop)
    return census_municipality_pops