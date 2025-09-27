

Previously, in sheet 3, there MCDONALD_BORO was erroneously listed as WESTMORELAND instead of WASHINGTON. This has been corrected.


# Counties/Munis with no reports

## 2015-2019

The following counties/municipalities have no reports for the 2015-2019 time frame:

| County | Municipality |
| :--- | :--- |
| INDIANA | CANOE TWP |
| BUTLER | PORTERSVILLE BORO |
| BEAVER | EASTVALE BORO |
| BEAVER | FRANKFORT SPRINGS BORO |

## 2020-2023

The following counties/municipalities have no reports for the 2020-2023 time frame (spot checked first 3 to confirm):

| County | Municipality |
| :--- | :--- |
| BEAVER | EASTVALE BORO |
| SOMERSET | BENSON BORO |
| BEAVER | HOMEWOOD BORO |
| SOMERSET | SHANKSVILLE BORO |
| BUTLER | PORTERSVILLE BORO |
| FAYETTE | FAYETTE CITY BORO |
| CAMBRIA | ASHVILLE BORO |
| WESTMORELAND | MADISON BORO |
| BEAVER | FALLSTON BORO |
| WASHINGTON | NEW EAGLE BORO |
| CAMBRIA | WILMORE BORO |
| LAWRENCE | SOUTH NEW CASTLE BORO |
| BEAVER | FRANKFORT SPRINGS BORO |
| WESTMORELAND | NEW ALEXANDRIA BORO |

# Counties/Munis with missing reports

## 2015-2019

The following 12 counties/municipalities have missing reports for the 2015-2019 time frame:

| County | Municipality | Count Missing |
| :--- | :--- | :--- |
| ALLEGHENY | MCDONALD BORO | 1 |
| BEAVER | ELLWOOD CITY BORO | 3 |
| BEAVER | FALLSTON BORO | 2 |
| BEAVER | HOMEWOOD BORO | 1 |
| CAMBRIA | ASHVILLE BORO | 2 |
| CAMBRIA | WILMORE BORO | 1 |
| FAYETTE | FAYETTE CITY BORO | 4 |
| SOMERSET | BENSON BORO | 2 |
| WASHINGTON | FINLEYVILLE BORO | 4 |
| WASHINGTON | NEW EAGLE BORO | 2 |
| WESTMORELAND | MADISON BORO | 1 |
| WESTMORELAND | NEW ALEXANDRIA BORO | 3 |


## 2020-2023

The following 21 counties/municipalities have missing reports for the 2020-2023 time frame:

| County | Municipality | Count Missing |
| :--- | :--- | :--- |
| ALLEGHENY | INGRAM BORO | 1 |
| ARMSTRONG | ELDERTON BORO | 1 |
| ARMSTRONG | FORD CLIFF BORO | 1 |
| BEAVER | ELLWOOD CITY BORO | 1 |
| BEAVER | WHITE TWP | 1 |
| BUTLER | WEST LIBERTY BORO | 1 |
| CAMBRIA | PATTON BORO | 3 |
| GREENE | SPRINGHILL TWP | 1 |
| INDIANA | CANOE TWP | 2 |
| INDIANA | MARION CENTER BORO | 3 |
| LAWRENCE | NORTH BEAVER TWP | 1 |
| LAWRENCE | SHENANGO TWP | 1 |
| LAWRENCE | TAYLOR TWP | 1 |
| SOMERSET | ADDISON BORO | 2 |
| SOMERSET | CONFLUENCE BORO | 1 |
| WASHINGTON | ALLENPORT BORO | 3 |
| WASHINGTON | DEEMSTON BORO | 1 |
| WASHINGTON | ELCO BORO | 1 |
| WASHINGTON | FINLEYVILLE BORO | 1 |
| WESTMORELAND | ADAMSBURG BORO | 1 |
| WESTMORELAND | ARNOLD CITY | 2 |


# Munis with anomalous errors

The following munis had reports which produced an error when attempting to access, as distinct from missing reports which are simply not available. 

## 2015-2019
| County | Municipality | Count Unavailable |
| :--- | :--- | :--- |
| ALLEGHENY | MCDONALD BORO | 1 |
| BEAVER | ELLWOOD CITY BORO | 3 |
| BEAVER | FRANKFORT SPRINGS BORO | 1 |
| WASHINGTON | FINLEYVILLE BORO | 1 |

## 2020-2023

| County | Municipality | Count Unavailable |
| :--- | :--- | :--- |
| BEAVER | ELLWOOD CITY BORO | 1 |
| BEAVER | FALLSTON BORO | 1 |
| BUTLER | PORTERSVILLE BORO | 1 |



# Data Integrity Checks Run

Not comprehensive of all checks
- Inspect county/muni combinations in Tab 1 not in Tab 2, and vice versa
- Inspect county/muni combinations in Tab 2 not in Tab 3, and vice versa
- Inspect county/muni combinations in Tab 1 not in Tab 3, and vice versa
- Check that Tab 2 and Tab 3 have same number of rows
- Pick location with high value of local/state/federal grants and total revenue, check that value corresponds to what is recorded in data
- Manually spot check county/munis with missing reports, confirming reports are missing
- Count all municipalities listed for each county in database, compare to number of municipalities listed on Annual Report web page
- Check codes listed in random reports in database against codes in Annual Reports as displayed on web page
- Check columns listed in original report are same as in new report, and in same order
- Spot check population estimates against Census API results