# pa_municipal_annual_financial_report_scraper

This scraper is used to download municipal annual financial reports from the Pennsylvania Department of Community and Economic Development's [Municipal Annual Financial Report Page](https://apps.dced.pa.gov/munstats-public/ReportInformation2.aspx?report=mAfrForm)

## Installation

```bash
pip install requirements.txt
```

## Usage

```bash
python pa_municipal_annual_financial_report_scraper.py
```
### Repository Notes
- This scraper:
    - will download the report for all counties, all municipalities, and all years specified in the `constants.py` page
    - can take an extended period of time to run (several hours), as it staggers downloads so as not to overwhelm the server or get blocked
    - may occasionally timeout and need to be restarted.
    - will store all files in the `downloads` directory
- Web scraping in general can be a brittle process. If the website changes, this scraper may break and need either to be updated or rewritten entirely.
- Partway through, I updated how I was organizing the database, which I documented using the alembic migrations. 

### Data Notes
- Municipalities are sometimes either lax in data reporting, or the source data is sometimes missing entirely. For example, Allegheny McDonald Boro AFRs from 2015-2019 all report 0 income of any type whatsoever. 

## How it Works
- The `scraper` uses Playwright to navigate to the website and download reports as excel files for all specified municipalities and years
- The `excel_processor` processes the excel files and stores the data in a sqlite database, using SQLAlchemy to interface with the database
  - The data processed are the totals defined in each row on "Sheet3" of the excel spreadsheet
- The `database_logic` uses SQLAlchemy to query the database
- The `report_creator` takes the data from the database and creates an Excel report

## Steps
1. Run `/scraper/main.py` until all reports are downloaded
2. Run `/excel_processor/main.py` until all reports are processed
3. Run `/database_logic/build_intermediate_table.py` to create an intermediate table
4. Run `/report_creator/main.py` to create the final report