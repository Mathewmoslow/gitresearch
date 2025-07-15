import pandas as pd

# Load raw data
df = pd.read_csv("data/Cleaned_Master_text.txt", sep=None, engine="python")
print("Original data:")
print(df[['Date']].head(10))
print(f"\nDate column type: {df['Date'].dtype}")

# Try parsing
df["Date"] = df["Date"].str.replace('_', ' ')
print("\nAfter underscore replacement:")
print(df[['Date']].head(10))

# Try to parse
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
print("\nAfter date parsing:")
print(df[['Date']].head(10))

# Check for non-null dates
print(f"\nNon-null dates: {df['Date'].notna().sum()} out of {len(df)}")
