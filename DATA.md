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
free text or mapping tables from codes to original values are included, and none were used in the analysis.
Injury information is limited to yes/no indicators. The source reports are public records released by the DMV;
because combinations of the remaining vehicle and crash attributes can be unique in a dataset of this size,
users must not attempt to re-identify individuals or link records to the source reports.

The full processed file (189 predictors) reproduces every number in the article and is available from the
authors on reasonable request for research use. Running the notebook on the public file reproduces
Supplementary Table S6 of the article, which shows that the conclusions are unchanged without the removed columns.
