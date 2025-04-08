#Part A.2
import pandas as pd
from re import fullmatch
from datetime import datetime

file_name = "time_series"
file_type = 'xlsx'

# gather indices of problematic rows - invalid, duplicates
#find all invalid timestamp rows
def is_valid_timestamp(timestamp):
    try:
        pd.to_datetime(timestamp)
        return True
    except:
        return False
    
def is_valid_value(value):
    try:
        pd.to_numeric(value)
        return pd.notna(value)
    except:
        return False

def find_invalid_timestamps(df):
    return df[~df['timestamp'].apply(is_valid_timestamp)]

#find all duplicate timestamp
def find_duplicates(df):
    return df[df.duplicated(subset="timestamp", keep='first')]

#extra check if duplicates have the same Value
def compare_duplicates(df):
    duplicates = find_duplicates(df)
    timestamp_duplicates = duplicates.groupby('timestamp')
    return timestamp_duplicates.filter(lambda x: len(x['value'].unique()) > 1)


#extra find all rows with Nan / not_a_number / ""
def find_invalid_values(df):
    return df[~df['value'].apply(is_valid_value)]

#run tests
def main():
    df = pd.read_excel(f"{file_name}.{file_type}", file_name, index_col=None)

    #part A.2.1#
    #timestamp validation
    invalid_ts = find_invalid_timestamps(df)
    if not invalid_ts.empty:
        print("Invalid Timestamps:")
        print(invalid_ts)
    else:
        print("All timestamps are valid.")

    #value validation
    invalid_vals = find_invalid_values(df)
    if not invalid_vals.empty:
        print("Invalid Values:")
        print(invalid_vals)
    else:
        print("All values are valid.")

    #duplicates validation
    duplicates = find_duplicates(df)
    if not duplicates.empty:
        print("Duplicated timestamps:")
        print(duplicates)

        duplicates = compare_duplicates(duplicates)
        if not duplicates.empty:
            print("Duplicated timestamps with different values:")
            print(duplicates) 
    else:
        print("All rows are completely distinct.")

    #part A.2.2
    df.drop_duplicates()
    print(df)
    print("Average of values per hour:")
    print(hourly_average(df))



# Part A.2.2
def hourly_average(df):
    df['timestamp_hours'] = pd.to_datetime(df['timestamp']).apply(lambda x: x.replace(minute=0, second=0, microsecond=0))
    avg_df = df[['timestamp_hours', 'value']].copy()
    
    avg_df['value'] = pd.to_numeric(df['value'], errors='coerce')
    avg_df.dropna(subset=['value'], inplace=True)
    
    avg_df.columns = ['start time', 'average value']
    avg_df.groupby('start time').mean()

    return avg_df

main()