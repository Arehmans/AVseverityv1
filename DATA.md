# Dataset: source, preprocessing and de-identification

## Source
The data are the processed autonomous-vehicle (AV) crash-severity dataset of Shafique et al.,
"Advancing Autonomous Vehicle Safety: Machine Learning to Predict Sensor-Related Accident Severity",
IEEE Access 12:25933–25948, 2024 (doi:10.1109/ACCESS.2024.3366990). It was compiled from the
"Report of Traffic Collision Involving an Autonomous Vehicle" (form OL 316) that AV manufacturers file with the
California Department of Motor Vehicles (DMV) and that the DMV publishes on its website. The dataset covers
reports from 2019–2022: 324 collisions, three damage-severity classes (Minor 237, Moderate 52, None 35).

## Preprocessing (done in the predecessor study; this study used its processed file unchanged)
* Each report was transcribed into one row.
* Check-box items of the form (for example damage location, collision type, lighting, road conditions,
  movement, injury flags) were converted into 0/1 indicator columns (171 binary predictors).
* Categorical and short text fields (manufacturer, make, model, registration location, county, city,
  vehicle 2 model, "other" specifications, and, in the full file only, address, date, time and the accident
  description) were label-encoded as integer codes. The codes have no ordinal meaning.
* Vehicle model years were kept as numbers (2 ordinal predictors).
* Missing values were handled as described in Shafique et al. (2024) before release; the processed file has no
  missing values.
* The article removes only the exported row-index column before analysis. All further steps (scaling, recursive
  feature elimination, oversampling) are fitted inside each training fold by the notebook.

## De-identification of the public file
`data/AV_crash_severity_deidentified.csv` differs from the full processed file only by the removal of these columns:

| Removed column | Reason |
|---|---|
| `Unnamed: 0` | exported row index (a record identifier) |
| `AccidentZIPcode` | five-digit ZIP code of the collision location |
| `AccidentADDRESS` | code of the street address (314 distinct values) |
| `AccidentDATE` | code of the collision date (271 distinct values) |
| `AccidentTIME` | code of the collision time (273 distinct values) |
| `AccDETAILS` | code of the free-text accident description (323 distinct values) |

Location is retained only as county and city (13 and 12 values) and time only as AM/PM.
No names, addresses, licence-plate or vehicle-identification numbers, driver's-licence numbers, dates of birth,
free text, record identifiers, or lookup tables or mappings from codes to original values are included in this
repository or in any of its releases, and none will be published. Injury information is limited to
yes/no indicators.

## Earlier versions of this repository
Versions of this repository published between 14 and 22 October 2026 contained the full processed file, including
the six columns removed above. To withdraw it, the original repository was deleted and this repository was recreated
without its earlier history; release v1.0 is its first version. The earlier commits, including those cited during
peer review, are therefore no longer available from this repository.

## Remaining linkage risk
All variables are derived from fields of the OL 316 reports that the California DMV itself publishes. Linking a row
to its source report would therefore not disclose any information beyond what that public report already contains,
and the data include no names, plates or contact details of the people involved. Nevertheless, because a few hundred
records are described by many attributes, combinations of the remaining vehicle and crash attributes (for example
manufacturer, county or city, the other vehicle's model and model year) can be unique, so linkage to the source report
cannot be ruled out entirely. Users must not attempt to identify individuals or to link records to the source reports.

## Access to the full file
The full processed file (189 predictors), which reproduces every number in the main analysis of the article, is not
public. It is available from the authors (corresponding author: Gyu Sang Choi) on reasonable request for
non-commercial research use, under the conditions that it is not redistributed and that no attempt is made to
identify individuals or link records to the source reports. Running the notebook on the public file reproduces
Supplementary Table S6 of the article, which shows that the conclusions are unchanged without the removed columns
(commands in `README.md`).
