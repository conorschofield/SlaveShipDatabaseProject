# excel-import (XLI)

This subfolder contains XLI, a Python package to import one or more input Excel files into the HCA 35 Index database. Due to the long and varied history of the Excel workbooks that contain the source data for the HCA 35, XLI applies a wide variety of data cleaning and cross-validation to mitigate human transcription error involved in indexing the thousands of records present in the HCA 35 record group. 

## Input

XLI reads any number of spreadsheet (`.xlsx`) files from a specified input directory. In practice, this means that if you transcribe a new HCA 35 volume, you can place the results of transcription in a new spreadsheet instead of trying to insert it into the original spreadsheet.

XLI reads the header rows of each sheet so as long as your field naming is consistent with the main HCA 35 Index (case sensitive and all), it'll read your files just fine even if you reoder the columns. However, it's recommended to just copy-paste the header from the main HCA 35 index.


## Output

XLI's primary output is to insert rows into an SQL database. XLI will **wipe** the tables it uses before inserting anything, so make sure you have the complete data set that you want in the database ready in Excel format before running.

In other words, XLI is best understood as a tool to create/recreate a SQL database from Excel files. The SQL database is meant to be fully read only in actual operation.


## A note on the source of truth

XLI has been very deliberately designed such that Excel files remain as the canonical source of truth. Software is rarely ever perfect and it is critical that it's always possible to audit the operation of XLI as needed. If XLI's output were to remain as the source of truth, it would be possible for an XLI bug that destroyed data to cause irreparable or infesible to repair damage to the data set. XLI guards against human error during transcription, but it can do little to guard against human error in the writing of its own code.


## Areas of improvement

- The handling of the statistics fields ("Men", "Women", "Boys", "Girls", and "Number of Slaves") discards some extra data contained in those cells (example: `166(164 Healthy and 2 Sickly)`), ideally we would be able to make use of that.
- Volume 62 inserts an extra column at index 13 for the "Captain", which we currently ignore. Maybe it's useful?
