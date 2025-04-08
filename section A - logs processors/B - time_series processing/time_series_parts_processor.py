#Part A.B
import pandas as pd
from re import fullmatch
from datetime import datetime, time
from os import makedirs, listdir

def parse_time(df, format):
    if format == "parquet":
        df.dropna(subset=['timestamp'], inplace=True)
        df['date'] = [datetime.date(day) for day in df['timestamp']]

    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)

        df['date'] = [datetime.date(day) for day in df['timestamp']]
        #df['time'] = [t.time() for t in df['timestamp']]

        #df.drop(columns=['timestamp'], inplace=True)
    return df

def split_file_by_date(file="time_series.xlsx"):

    file_name, file_type = file.split('.')

    if file_type == 'parquet':
        df = pd.read_parquet(f"{file_name}.{file_type}", engine="pyarrow")
    elif file_type == 'xlsx':
        df = pd.read_excel(f"{file_name}.{file_type}", file_name, index_col=None)
    elif file_type == 'csv':
        df = pd.read_csv(f"{file_name}.{file_type}", file_name, index_col=None)
    else:
        raise ValueError(f"The format {file_type} is yet to be supported...")

    df = parse_time(df, file_type)
    
    output_path = 'sub_series_by_dates'
    makedirs(output_path, exist_ok=True)
    for date, sub_df in df.groupby('date'):
        sub_df.drop(columns=['date'], inplace=True)
        sub_df.to_csv(f"{output_path}/{date}.csv", index=False, sep=';')

    return output_path




# gather indices of problematic rows - invalid, duplicates
def is_valid_timestamp(timestamp):
    try:
        pd.to_datetime(str(timestamp))
        return True
    except:
        return False
    
def is_valid_value(value):
    try:
        pd.to_numeric(value)
        return pd.notna(value)
    except:
        return False

#find all invalid timestamp
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
def run_tests(df):
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

        #duplicated timestamps with different values
        duplicates = compare_duplicates(duplicates)
        if not duplicates.empty:
            print("Duplicated timestamps with different values:")
            print(duplicates) 
    else:
        print("All rows are completely distinct.")

def main():
    processable_files = [f for f in listdir() if '.' in f and f.split('.')[1].lower() in ["xlsx", "parquet", "csv"]]
    for f in processable_files:
        print(f)
    file = input("Which file would you like to process?\t")

    subfiles_path = split_file_by_date(file) + '\\'
    
    overall_avg_df = pd.DataFrame()
    for subfile in listdir(subfiles_path):
        if not subfile.endswith('.csv'):
            continue

        date = subfile[:-4]
        df = pd.read_csv(subfiles_path + subfile, sep=';')
        print(df.head())

        print(f"\nRunning tests for date: {date}")
        run_tests(df)

        #calculate
        avg_df = hourly_average(df)

        overall_avg_df = pd.concat([overall_avg_df, avg_df], ignore_index=True)

    overall_avg_df.to_csv("combined_hourly_averages.csv", index=False, sep=';')




# Part A.B.1.2
def hourly_average(df):
    df['timestamp_hours'] = pd.to_datetime(df['timestamp']).apply(lambda x: x.replace(minute=0, second=0, microsecond=0))
    avg_df = df[['timestamp_hours', 'value']].copy()
    
    avg_df['value'] = pd.to_numeric(df['value'], errors='coerce')
    avg_df.dropna(subset=['value'], inplace=True)
    
    avg_df.columns = ['start time', 'average value']
    avg_df.groupby('start time').mean()

    return avg_df

main()


'''
PARQUET > CSV
parquet is better when it comes to querying, since it saves only by columns and not by rows as CSV does,
which makes querying more efficient.
Also it's a compressed format, meaning it's unreadable to us without proper applications, yet it takes less storage space.
'''