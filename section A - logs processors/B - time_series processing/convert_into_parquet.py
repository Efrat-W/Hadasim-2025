from pandas import read_excel, read_csv, to_numeric

def file_to_parquet(file):
    file_name, file_format = file.split('.')
    if file_format == "xlsx":
        df = read_excel(file)
    elif file_format == "csv":
        df = read_csv(file)
    
    df['value'] = to_numeric(df['value'], errors='coerce')
    df.dropna(inplace=True)


    parquet_file = file_name + '.parquet'

    # Convert to parquet using pyarrow engine
    df.to_parquet(parquet_file, engine='pyarrow', index=False)

file = "time_series.xlsx"
file_to_parquet(file)