# %%
import pandas as pd
import numpy as np

# Set display options for better console output
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Load the dataframe
df = pd.read_csv('cardio_train.csv', delimiter=';')

print("--- Successfully loaded cardio_train.csv ---")
print(f"Original DataFrame shape: {df.shape}\n")
print("Original DataFrame head:")
print(df.head())
print("\n" + "="*80 + "\n")

# Made 'gender' more readable (1: Female, 2: Male)
df['gender'] = df['gender'].map({1: 'Female', 2: 'Male'})
# Trim the DataFrame to a smaller sample
wide_df = df[['id', 'age', 'gender', 'ap_hi', 'ap_lo']]

print("--- Created a narrower sample (LESS COLUMNS) for Melt/Pivot ---")
print(wide_df.head(10))
print("\n" + "="*80 + "\n")

# 1. Melt
# I keep 'id', 'age', and 'gender' as identifier variables using 'id_vars'.
# 'value_vars' are the columns I want to melt.
# I melt 'ap_hi' (systolic) and 'ap_lo' (diastolic) into two new columns:
# 'pressure_type' (which will contain 'ap_hi' or 'ap_lo')
# 'pressure_value' (which will contain the corresponding value from those columns that are now melted)

print("--- 1. DEMONSTRATING melt() ---")
melted_df = wide_df.melt(
    id_vars=['id', 'age', 'gender'],
    value_vars=['ap_hi', 'ap_lo'],
    var_name='pressure_type',
    value_name='pressure_value'
)
print("Melted DataFrame (long format):")
print(melted_df)
print("\n" + "="*80 + "\n")


# 2. Pivot
# I use pivot to restore our 'melted_df' back to its original structure.
# - index: The column(s) to use as the new DataFrame's index. (id, age, gender)
# - columns: The column to use to create the new DataFrame's columns.
# - values: The column to use for populating the new DataFrame's values.

print("--- 2. DEMONSTRATING pivot() ---")
pivoted_df = melted_df.pivot(
    index=['id', 'age', 'gender'],
    columns='pressure_type',
    values='pressure_value'
)
# .reset_index() is used to turn the index columns back into regular columns for easier viewing
pivoted_df = pivoted_df.reset_index().rename_axis(None, axis=1) 

print("Pivoted DataFrame (wide format, restored from melt):")
print(pivoted_df)
print("\n" + "="*80 + "\n")


# 3. Groupby
# 'groupby' is used for splitting the data into groups based on some criteria.
# It creates a 'DataFrameGroupBy' object. 

print("--- 3. DEMONSTRATING groupby() ---")
# I group by 'gender' (1=Female, 2=Male) and 'cholesterol' (1, 2, 3)
grouped_data = df.groupby(['gender', 'cholesterol'])

print(f"Created a DataFrameGroupBy object: {type(grouped_data)}")
#showing the list that is created when the dataframegroupby element is created
print("Groups found (first 5):")
print(list(grouped_data.groups.keys())[:5])

# Show the size of each group
print("\nSize of each group (gender, cholesterol):")
print(grouped_data.size())
print("\nDescriptive statistics for each group: (gender broken down by cholesterol)")
print(grouped_data.describe())
print("\n" + "="*80 + "\n")


# 4. Aggregation (agg)
# I can apply different functions to different columns.

print("--- 4. DEMONSTRATING Aggregation (.agg()) ---")
# I will calculate:
# - The mean 'weight' and 'height'
# - The median 'ap_hi' (systolic pressure)
# - The total count of smokers ('smoke' column, where 1=smoker)

aggregations = {
    'weight': ['mean', 'std'],
    'height': ['mean', 'std'],
    'ap_hi': 'median',
    'smoke': 'sum' 
}

aggregated_df = grouped_data.agg(aggregations)

#Using round function for cleaner output
aggregated_df = aggregated_df.round(2)

print("Aggregated results (mean and std weight/height, median ap_hi, total smokers):")
print(aggregated_df)
print("\n" + "="*80 + "\n")


# 5. Iteration (iterrows)
# 'iterrows' iterates over DataFrame rows as (index, Series) pairs.


print("--- 5. DEMONSTRATING Iteration (.iterrows()) ---")
print("Iterating over the *first 5 rows* of the main DataFrame:")

# use .head(5) to only iterate over a small sample due to .iterrows() being slow and also the amount of output if the entire df is used
for index, row in df.head(5).iterrows():
    print(f"\nRow Index: {index}")
    print(f"  ID: {row['id']}")
    print(f"  Age (days): {row['age']}")
    print(f"  Weight: {row['weight']}")
    print(f"  Cardio risk (1=yes): {row['cardio']}")



