import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from sklearn.preprocessing import MinMaxScaler

random.seed(22)


def generate_time_series(start_date, end_date, freq):
    """
    Generate a time index (DatetimeIndex) with the specified frequency.

    Parameters:
        start_date (datetime): The start date of the time index.
        end_date (datetime): The end date of the time index.
        freq (str): The frequency for the time index (e.g., '10T' for 10 minutes, '1H' for hourly, 'D' for daily).

    Returns:
        DatetimeIndex: The generated time index.
    """
    date_rng = pd.date_range(start=start_date, end=end_date, freq=freq)
    return date_rng


def add_weekly_seasonality(data, seasonality, season_type):
    """
    Add weekly seasonality component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

    Returns:
        numpy.ndarray: The seasonal component of the time series.
    """
    if seasonality == "exist":  # Weekly Seasonality
        seasonal_component = np.sin(2 * np.pi * data.dayofweek / 7)
        seasonal_component += 1 if season_type == 'multiplicative' else 0
    else:
        seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
    return pd.Series(seasonal_component)


def add_daily_seasonality(data, seasonality, season_type):
    """
    Add seasonality component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

    Returns:
        numpy.ndarray: The seasonal component of the time series.
    """
    if seasonality == "exist":  # Daily Seasonality
        seasonal_component = np.sin(2 * np.pi * data.hour / 24)
        seasonal_component += 1 if season_type == 'multiplicative' else 0
    else:
        seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
    return pd.Series(seasonal_component)


def add_trend(data, trend, data_size, data_type):
    """
    Add trend component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        trend (str): The magnitude of the trend ('No Trend', 'Small Trend', 'Large Trend').

    Returns:
        numpy.ndarray: The trend component of the time series.
    """
    if trend == "exist":
        slope = random.choice([1, -1])
        trend_component = np.linspace(0, data_size / 30 * slope, len(data)) if slope == 1 else np.linspace(
            -1 * data_size / 30, 0, len(data))
    else:  # No Trend
        trend_component = np.zeros(len(data)) if data_type == 'additive' else np.ones(len(data))

    return pd.Series(trend_component)


def add_cycles(data, cyclic_periods, season_type):
    """
    Add cyclic component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        cyclic_periods (str): The type of cyclic periods ('No Cyclic Periods', 'Short Cycles', or 'Long Cycles').

    Returns:
        numpy.ndarray: The cyclic component of the time series.
    """
    if cyclic_periods == "exist":  # Quarterly
        cycle_component = 1 if season_type == 'multiplicative' else 0
        cycle_component += np.sin(2 * np.pi * (data.quarter-1) / 4)
    else:  # No Cyclic Periods
        cycle_component = 0 if season_type == 'additive' else 1

    return cycle_component


def add_missing_values(data, percentage_missing=0.05):
    """
    Add missing values to the time series data within a specified date range.

    Parameters:
        data (numpy.ndarray): The time series data.
        percentage_missing (Float): percentage of missing value.

    Returns:
        numpy.ndarray: The time series data with missing values.
    """
    num_missing = int(len(data) * percentage_missing)
    missing_indices = np.random.choice(len(data), size=num_missing, replace=False)

    data_with_missing = data.copy()
    data_with_missing[missing_indices] = np.nan

    return data_with_missing


def add_noise(data, noise_level):
    """
    Add noise component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        noise_level (str): The magnitude of noise ('No Noise', 'Small Noise', 'Intermediate Noise', 'Large Noise').

    Returns:
        numpy.ndarray: The noise component of the time series.
    """
    if noise_level == "small":
        noise_level = 0.1
        # noise = np.random.normal(0, 0.05, len(data))
    elif noise_level == "large":
        noise_level = 0.3
        # noise = np.random.normal(0, 0.1, len(data))
    else:  # No Noise
        noise_level = 0

    noise = np.zeros_like(data)
    for i in range(len(data)):
        noise[i] = np.random.normal(0, abs(data[i]) * noise_level) if noise_level > 0 else 0
    return pd.Series((data + noise)[:, 0])


def add_outliers(data, percentage_outliers=0.05):
    """
    Add outliers to the time series data.

    Parameters:
        data (numpy.ndarray): The time series data.
        percentage_outliers (float): The percentage of outliers to add (e.g., 0.2 for 20%).

    Returns:
        numpy.ndarray: The time series data with outliers.
    """
    # data = pd.Series(data)
    num_outliers = int(len(data) * percentage_outliers)
    outlier_indices = np.random.choice(len(data), num_outliers, replace=False)
    # data_with_outliers = pd.Series(data.copy())
    data_with_outliers = data.copy()
    outliers = np.random.uniform(-1, 1, num_outliers)
    anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
    if len(outliers) > 0:
        data_with_outliers[outlier_indices] = outliers
        anomaly_mask[outlier_indices] = True

    return data_with_outliers, anomaly_mask


def main():
    # Define simulation parameters
    start_date = datetime(2021, 7, 1)
    frequencies = ["1D", "10T", "30T", "1H", "6H", "8H"]
    daily_seasonality_options = ["no", "exist"]
    weekly_seasonality_options = ["exist", "no"]
    noise_levels = ["small"]  # , "large"]
    trend_levels = ["exist", "no"]
    cyclic_periods = ["exist", "no"]
    data_types = [""
                  "", "additive"]
    percentage_outliers_options = [0.05]  # , 0]
    data_sizes = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]
    meta_data = []
    counter = 0
    # for freq in frequencies:
    for daily_seasonality in daily_seasonality_options:
        for weekly_seasonality in weekly_seasonality_options:
            for noise_level in noise_levels:
                for trend in trend_levels:
                    for cyclic_period in cyclic_periods:
                        for percentage_outliers in percentage_outliers_options:
                            for data_type in data_types:
                                for _ in range(16):
                                    # for data_size in data_sizes:
                                    data_size = random.choice(data_sizes)
                                    freq = random.choice(frequencies)
                                    counter += 1
                                    file_name = f"TimeSeries_daily_{daily_seasonality}_weekly_{weekly_seasonality}_noise_{noise_level}_trend_{trend}_cycle_{cyclic_period}_outliers_{int(percentage_outliers * 100)}%_freq_{freq}_size_{data_size}Days.csv"
                                    print(f"File '{file_name}' generated.")
                                    # Generate time index
                                    date_rng = generate_time_series(start_date, start_date + timedelta(days=data_size),
                                                                    freq)
                                    # Create components
                                    daily_seasonal_component = add_daily_seasonality(date_rng, daily_seasonality,
                                                                                     season_type=data_type)
                                    weekly_seasonal_component = add_weekly_seasonality(date_rng, weekly_seasonality,
                                                                                       season_type=data_type)
                                    trend_component = add_trend(date_rng, trend, data_size=data_size,
                                                                data_type=data_type)
                                    cyclic_period = "exist"
                                    cyclic_component = add_cycles(date_rng, cyclic_period, season_type=data_type)

                                    # Combine components and add missing values and outliers
                                    if data_type == 'multiplicative':
                                        data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
                                    else:
                                        data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component
                                    # Create a MinMaxScaler instance
                                    scaler = MinMaxScaler(feature_range=(-1, 1))
                                    data = scaler.fit_transform(data.values.reshape(-1, 1))
                                    data = add_noise(data, noise_level)
                                    data, anomaly = add_outliers(data, percentage_outliers)
                                    data = add_missing_values(data, 0.05)

                                    # Save the data to a CSV file
                                    df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
                                    df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)

                                    """
                                    import matplotlib.pyplot as plt
                                    plt.figure(figsize=(10, 6))
                                    # Plot the time series data
                                    plt.plot(df['timestamp'], df['value'], marker='o', linestyle='-', color='b',
                                             label='Time Series Data')
                                    # Add labels and title
                                    plt.xlabel('Time')
                                    plt.ylabel('Value')
                                    plt.title('Time Series Plot')
                                    plt.legend()
                                    # Display the plot
                                    plt.tight_layout()
                                    plt.show()
                                    break
                                    """

                                    meta_data.append({'id': str(counter) + '.csv',
                                                      'data_type': data_type,
                                                      'daily_seasonality': daily_seasonality,
                                                      'weekly_seasonality': weekly_seasonality,
                                                      'noise (high 30% - low 10%)': noise_level,
                                                      'trend': trend,
                                                      'cyclic_period (3 months)': cyclic_period,
                                                      'data_size': data_size,
                                                      'percentage_outliers': percentage_outliers,
                                                      'percentage_missing': 0.05,
                                                      'freq': freq})
                                    # generate_csv(list(zip(date_rng, data)), file_name)

    meta_data_df = pd.DataFrame.from_records(meta_data)
    meta_data_df.to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    main()
