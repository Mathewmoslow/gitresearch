# Scripts Documentation

## Column Naming Convention
- All duration data in CSV files uses the column name `duration_hours`
- Plot labels may show "Hours" or "Total Hours" for readability
- The column "Total_Hours" is only used in aggregated summaries, not raw data

## Data Flow
1. clean_data.py creates CSVs with `duration_hours` column
2. Analysis scripts read `duration_hours` and aggregate as needed
3. Visualizations may use "Hours" in titles/labels for clarity
