from enum import Enum


class MunicipalityClasses(Enum):
    FIRST_TOWNSHIP = "1st Township"
    SECOND_TOWNSHIP = "2nd Township"
    THIRD_TOWNSHIP = "3rd Township"
    BOROUGH = "Borough"
    FIRST_CITY = "1st City"
    SECOND_CITY = "2nd City"
    THIRD_CITY = "3rd City"

MUNICIPALITY_CLASS_VALUES: list[str] = [member.value for member in MunicipalityClasses]

class UrbanRural(Enum):
    URBAN = "Urban"
    RURAL = "Rural"

URBAN_RURAL_VALUES: list[str] = [member.value for member in UrbanRural]

class Year(Enum):
    Y2015 = 2015
    Y2016 = 2016
    Y2017 = 2017
    Y2018 = 2018
    Y2019 = 2019
    Y2020 = 2020
    Y2021 = 2021
    Y2022 = 2022
    Y2023 = 2023

YEAR_VALUES: list[int] = [member.value for member in Year]

class SheetName(Enum):
    METADATA = "METADATA"
    YEAR_AND_MUNI = "1) Grant $ by year & muni"
    FIVE_YEAR_AVG = "2) 5yr avg grant $ by muni"
    TOTAL_PER_CAP_PCT_REV = "3) 5yr total, per cap, and % re"

class YearCond(Enum):
    Y2015_2019 = "<= 2019"
    Y2020_2023 = ">= 2020"