import seaborn
import pandas as pd
import numpy as np

# load csv file
london_data = pd.read_csv('weather_london.csv')

# Explore the Data
# take a look at london_data dataset
print(london_data.head())
print(london_data.iloc[100:200])

# data points size
print(london_data.shape)
print(len(london_data))

# Looking At Temperature
temp = london_data['TemperatureC']
# print(temp.min(), temp.max())
print(np.min(temp), np.max(temp))

# average temperatures
avg_temp = np.mean(temp)
print(avg_temp)  # avg temp is 12.08 C

# variance of temp
temp_var = np.var(temp)
print(temp_var)  # variance is 29.72

# standard deviation of temp
temp_std_dev = np.std(temp)
print(temp_std_dev)  # std dev is 5.45

# Filter by month
print(london_data.month.head())
print(london_data.month.tail())
# june temp
june = london_data.loc[london_data["month"] == 6]["TemperatureC"]
print(june)
# july temp
july = london_data.loc[london_data["month"] == 7]["TemperatureC"]
print(july)

# avg temp for june and july
print(np.mean(june))  # june avg temp: 17.05
print(np.mean(july))  # july avg temp: 18.78

# std dev june and july
print(np.std(june))  # std dev june: 4.60
print(np.std(july))  # std dev july: 4.14

# month average temp and std deviation
for i in range(1, 13):
    month = london_data.loc[london_data["month"] == i]["TemperatureC"]
    print("The mean temperature in month " + str(i) + " is " + str(np.mean(month)))
    print("The standard deviation of temperature in month " + str(i) + " is " + str(np.std(month)) + "\n")


# # Explore Your Own
# hourly average precipitation
for i in range(0, 24):
    hour = london_data.loc[london_data["hour"] == i]["dailyrainMM"]
    print("The mean precipitation in hour "+str(i) + " is " + str(np.mean(hour)))

# avg rain by hour
avg_rain_hour = london_data.groupby(['hour'])['dailyrainMM'].mean()
print(avg_rain_hour)


# avg temp by month using groupby
avg_temp_month = london_data.groupby(['month'])['TemperatureC'].mean().round(2)
print("Avg Temp by Month:", avg_temp_month)

# standard deviation of temp by month using groupby
std_temp_month = london_data.groupby(['month'])['TemperatureC'].apply(np.std).round(2)
print("Standard Deviation Temp by Month:", std_temp_month)

# Combine avg_temp_month and std_temp_month into a single DataFrame
combined_df = pd.concat([avg_temp_month, std_temp_month], axis=1)
combined_df.columns = ['Avg Temperature (C)', 'Standard Deviation']

print(combined_df)

# avg wind speed (kmh) by month
avg_windspkmh_month = london_data.groupby(['month'])['WindSpeedKMH'].mean()
# avg humidity by month
avg_humidity_month = london_data.groupby(['month'])['Humidity'].mean()
# avg daily rain by month
avg_dailyrain_month = london_data.groupby(['month'])['dailyrainMM'].mean()

combined_df['Wind Speed (KMH)'] = avg_windspkmh_month.round(2)
combined_df['Humidity'] = avg_humidity_month.round(2)
combined_df['Daily Rain (MM)'] = avg_dailyrain_month.round(2)

print(combined_df)


# Pivot Table Temperatures by Month-Hour
# avg temp by month hours
avg_temp_month_hour = london_data.groupby(['month', 'hour'])['TemperatureC'].mean().round(2)
# Reset index to convert the multi-index into columns
avg_temp_month_hour = avg_temp_month_hour.reset_index()
# Pivot the DataFrame to display rows by month and columns by hour
pivot_temp = avg_temp_month_hour.pivot(index='month', columns='hour', values='TemperatureC')
print(pivot_temp)
# Rename index to display month names (assuming you have a mapping of month numbers to their abbreviated names)
month_names = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT',
               11: 'NOV', 12: 'DEC'}
pivot_temp = pivot_temp.rename(index=month_names)
# Add a row for the total of each column
pivot_temp.loc['Total_avg'] = pivot_temp.mean(axis=0).round(2)
# Calculate the percentage of total sum for each hour
mean_row = pivot_temp.loc['Total_avg']
percent_row = (mean_row / mean_row.sum())

print(pivot_temp)

# max value by column total
print(pivot_temp.loc['Total_avg'].idxmax())  # hour 14 have the highest temparature rate


# Pivot Table Precipitation (MM) by Month-Hour
# avg temp by month hours
avg_rain_month_hour = london_data.groupby(['month', 'hour'])['dailyrainMM'].mean().round(2)
# Reset index to convert the multi-index into columns
avg_rain_month_hour = avg_rain_month_hour.reset_index()
# Pivot the DataFrame to display rows by month and columns by hour
pivot_rain = avg_rain_month_hour.pivot(index='month', columns='hour', values='dailyrainMM')
print(pivot_rain)
# Rename index to display month names (assuming you have a mapping of month numbers to their abbreviated names)
month_names = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT',
               11: 'NOV', 12: 'DEC'}
pivot_rain = pivot_rain.rename(index=month_names)
# Add a row for the total of each column
pivot_rain.loc['Total_avg'] = pivot_rain.mean(axis=0).round(2)
# Append the percentage row to the pivot table
pivot_rain = pivot_rain.append(percent_row.round(2))

print(pivot_rain)

# max value by column total
print(pivot_rain.loc['Total_avg'].idxmax())  # hour 22 have the highest rain rate
