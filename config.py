



"""
Excel Information
These represent information needed for parsing details from the excel report
"""
# Sheet Name: The sheet the revenue information is on
SHEET_NAME = "Sheet3"
# Column Names: The column values (1-indexed) for the code, label, and total
CODE_COLUMN = 1
LABEL_COLUMN = 2
TOTAL_COLUMN = 10

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

LOCAL_CODES = [
    '357.01',
    '357.02',
    '357.03',
    '357.XX'
]