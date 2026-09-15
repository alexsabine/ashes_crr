# Ledger

One row per committed prediction, in pre-registration order. Rows are
appended, never edited; a correction is a new row that references the old
id. "Observed" is given at full precision and rounded. Every row links to
the script that printed the number and the log it printed it in.

| id | prereg hash (short) | dataset (unseen? Y/N) | prediction | threshold | observed | per-unit pass fraction | verdict | script | log |
|---|---|---|---|---|---|---|---|---|---|
