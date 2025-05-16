import pandas as pd
import matplotlib.pyplot as plt

def read_glucose_data(file_path):
    """
    Reads glucose data from a CSV file and returns it as a pandas DataFrame.
    """
    # second row is the header
    df = pd.read_csv(file_path, header=1)
    # Convert 'Device Timestamp' to datetime
    df['Device Timestamp'] = pd.to_datetime(df['Device Timestamp'], dayfirst=True, errors='coerce')

    # row 3 to 263 is data
    df_2022 = df.iloc[2:261]
    df_2023 = df.iloc[262:1347]
    df_2024 = df.iloc[1348:2445]
    df_2025 = df.iloc[2446:4416]
    
    return df_2022, df_2023, df_2024, df_2025


def filter_glucose_data(df):
    """
    Filters glucose data using a low pass butterworth filter.
    """
    
    return df

def plot_glucose_data(df, year, start=0, end=500):
    """
    Plots glucose data for a given year.
    X-axis shows only 3-hour intervals (00:00, 03:00, ..., 21:00), 
    and data points are plotted at their actual times.
    Background color alternates for each day, aligned to the x-axis (midnight to midnight).
    """
    import matplotlib.dates as mdates

    df = df.iloc[start:end].copy()
    df['Time'] = df['Device Timestamp'].dt.strftime('%H:%M')
    df['Date'] = df['Device Timestamp'].dt.strftime('%Y-%m-%d')
    df['Datetime'] = df['Device Timestamp']

    glucose = pd.to_numeric(df['Historic Glucose mmol/L'], errors='coerce')

    plt.figure(figsize=(14, 6))
    ax = plt.gca()

    # Plot using actual datetime for x-axis
    ax.plot(df['Datetime'], glucose, linestyle='-')

    plt.title(f'Glucose Levels in {year} (3-hour X-axis)')
    plt.xlabel('Time')
    plt.ylabel('Glucose Level (mmol/L)')
    plt.grid()

    # Set x-ticks at every 3 hours
    locator = mdates.HourLocator(byhour=range(0,24,3))
    formatter = mdates.DateFormatter('%H')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # Add background color for each day, aligned to the x-axis (midnight to midnight)
    colors = ["#20c2a7", "#cd56d8"]  # alternate colors
    if not df['Datetime'].isnull().all():
        min_dt = df['Datetime'].min().replace(hour=0, minute=0, second=0, microsecond=0)
        max_dt = df['Datetime'].max().replace(hour=0, minute=0, second=0, microsecond=0) + pd.Timedelta(days=1)
        num_days = (max_dt - min_dt).days
        for i in range(num_days):
            day_start = min_dt + pd.Timedelta(days=i)
            day_end = day_start + pd.Timedelta(days=1)
            ax.axvspan(day_start, day_end, color=colors[i % len(colors)], alpha=0.2)

    # Add date labels below the x-axis at the start of each day
    for i in range(num_days):
        day_start = min_dt + pd.Timedelta(days=i)
        ax.annotate(
            (day_start).strftime('%Y-%m-%d'),
            xy=(day_start, ax.get_ylim()[0]),
            xytext=(0, -30),
            textcoords='offset points',
            ha='center',
            va='top',
            fontsize=9,
            color='blue',
            rotation=0
        )

    plt.tight_layout()
    plt.show()

def main():
    # File path to the glucose data CSV file
    file_path = 'glucose_data/glucose_data.csv'
    
    # Read the glucose data
    df_2022, df_2023, df_2024, df_2025 = read_glucose_data(file_path)
    
    # Plot the glucose data for each year
    plot_glucose_data(df_2022, '2022')
    plot_glucose_data(df_2023, '2023')
    plot_glucose_data(df_2024, '2024')
    plot_glucose_data(df_2025, '2025')

if __name__ == "__main__":
    main()
