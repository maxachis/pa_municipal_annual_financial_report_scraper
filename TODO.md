

# Complete current dataset for 10-county region from 2015-2019
- [ ] Add Glenfield Boro in Allegheny County's Financial Reports 
- [X] Scrape total revenue % for each year from the annual financial reports
    - [X] Add to Existing Tab 1) Grant $ by year & muni
        - [X] Total Revenue
- [X] Calculate 5-year revenue total for each muni
    - [X] Add to highlighted Column In Tab 3) 5yr total, per cap, and % rev grant $ by muni
        - [X] TOTAL REVENUE 5-YEAR TOTAL
- [X] Calculate % of total revenue for Federal, State, Local, and All Grants
    - Note: I am assuming this means what percent of total revenue are each of the grants
    Add to highlighted Columns In Tab 3) 5yr total, per cap, and % rev grant $ by muni
        - [X] % REV FED GRANTS
        - [X] % REV STATE GRANTS
        - [X] % REV LOCAL GRANTS
        - [X] % REV ALL GRANTS
- [ ] Double-check completeness/accuracy of total revenue number with a few random checks
    - [ ] Calculate total number of expected municipalities for each county
        - [ ] Compare with actual number of expected municipalities for each county
    - [ ] Spot check 5 county/municipalities, selected at random, and reconstruct those values from the reports, ensuring they align with what is reported in the document

# Extend Current 2015-2019 dataset to include Cambria and Somerset counties
- [X] Integrate into existing tabs 1-3 on current dataset
    - [X] To complete this, must also download and merge some additional data that lives on tabs 2 & 3 that come from sources other than the annual financial reports:
        - [X] Population
        - [X] Muni Classification
        - [X] Urban Rural Population
    - [X] Use the data sources specified in the metadata tab to 
- [ ] Check/clean data for Cambria and Somert counties
    - [ ] For munis with more than 0 but fewer than all 5 reports available, include on tab 1 but highlight these rows in a manner comparable to how they are currently formatted. 
    - [ ] Munis with less than all 5 annual financial reports should not be included on tab 2 or tab 3
    - [ ] Munis with 0 reports submitted for the timeframe should be left off the dataset entirely
        - [ ] Note Munis excluded (for either reason) from the dataset on the metadata tab

# Extend 12-county dataset to include years 2020-2023
- [X] Extend to include years 2020, 2021, 2022, and 2023
- [X] DO NOT integrate with existing dataset
    - [X] Instead, create a new dataset, set up in the same way and formatted the same, but just includes the 2020-2023 data.
- [ ] Check/clean data as needed, following same guidelines as above for munis that are missing some or all annual reports for the time frame 


# Get Additional Data Sources

- [X] Population
- [X] Muni Classification
- [X] Urban Rural Classification