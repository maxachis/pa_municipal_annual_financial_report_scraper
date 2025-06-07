"""
Configuration

This file contains various configuration variables for the scraper
"""
from openpyxl.xml.constants import REL_NS

"""
Excel Information
These represent information needed for parsing details from the excel report
"""
# Sheet Name: The sheet the revenue information is on
REPORT_RELEVANT_SHEET_NAME = "Sheet3"
JOINED_POP_RELEVANT_SHEET_NAME = "Sheet1"
# Column Names: The column values (1-indexed) for the code, label, and total
REL_CODE_COLUMN = 1
REL_LABEL_COLUMN = 2
REL_TOTAL_COLUMN = 10

JOINED_GEO_COLUMN=1
JOINED_MUNI_COLUMN=2
JOINED_COUNTY_COLUMN=3
JOINED_CLASS_COLUMN=5
JOINED_POP_ESTIMATE_COLUMN=6
JOINED_POP_MARGIN_COLUMN=7
JOINED_URBAN_RURAL_COLUMN=8
"""
Scraper Information

Indicates what information will be scraped

"""
# Counties to be scraped. Must match the labels as they appear in the Counties dropdown
COUNTIES = [
    "ALLEGHENY",
    "ARMSTRONG",
    "BEAVER",
    "BUTLER",
    "FAYETTE",
    "GREENE",
    "INDIANA",
    "LAWRENCE",
    "WESTMORELAND",
    "WASHINGTON"
]
# Years to be scraped
YEARS = ["2015", "2016", "2017", "2018", "2019"]

"""
Code Classification
Classifies codes according to whether they are federal, state, or local
This is used when determining the total for each code
"""
FEDERAL_PREFIX = "351"
FEDERAL_CODES = [
    '351.01',
    '351.02',
    '351.03',
    '351.04',
    '351.05',
    '351.06',
    '351.07',
    '351.08',
    '351.09',
    '351.1',
    '351.11',
    '351.12',
    '351.13',
    '351.XX'
]
STATE_PREFIX = "354"
STATE_CODES = [
    '354.01',
    '354.02',
    '354.03',
    '354.04',
    '345.05',
    '345.06',
    '345.07',
    '345.08',
    '354.09',
    '354.1',
    '354.11',
    '354.12',
    '354.13',
    '354.14',
    '354.15',
    '354.XX',
    '355.08'
]
LOCAL_PREFIX = "357"
LOCAL_CODES = [
    '357.01',
    '357.02',
    '357.03',
    '357.XX'
]