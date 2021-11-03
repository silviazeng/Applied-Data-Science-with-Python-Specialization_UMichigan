#----------Assignment 2----------
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to Preview the Grading for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# An NOAA dataset has been stored in the file data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) Daily Global Historical Climatology Network (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# Each row in the assignment datafile corresponds to a single observation.
# The following variables are provided to you:
  # id : station identification code
  # date : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
  # element : indicator of element type
  # TMAX : Maximum temperature (tenths of degrees C)
  # TMIN : Minimum temperature (tenths of degrees C)
  # value : data value for element (tenths of degrees C)
# For this assignment, you must:
# Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# The data you have been given is near Ann Arbor, Michigan, United States, and the stations the data comes from are shown on the map below.

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):
    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))
    station_locations_by_hash = df[df['hash'] == hashid]
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()
    plt.figure(figsize=(8,8))
    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)
    return mplleaflet.display()
leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# 1. Preprocessing Data:
import pandas as pd
import numpy as np

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv').sort_values('Date')
df['Data_Value'] = df['Data_Value'].apply(lambda x: x/10)
df['Date'] = df['Date'].apply(pd.to_datetime)

  # unstack MAX and MIN
df_max = df[df['Element'] =='TMAX'].rename(columns = {'Data_Value':'Max'}).drop(['Element'], axis=1)
df_min = df[df['Element'] =='TMIN'].rename(columns = {'Data_Value':'Min'}).drop(['Element'], axis=1)

DF = pd.merge(df_max, df_min)
DF = DF.groupby('Date').agg({'Max':np.max, 'Min':np.min}).reset_index()

  # extract year, month, day; drop feb 29
DF['Year'] = pd.to_numeric(DF['Date'].dt.year)
DF['Month'] = pd.to_numeric(DF['Date'].dt.month)
DF['Day'] = pd.to_numeric(DF['Date'].dt.day)

DF = DF.drop(DF[(DF['Month']==2) & (DF['Day'] == 29)].index)

  # divide and conquer
DF_2005to2014 = DF[(DF['Year']>=2005) & (DF['Year']<2015)]
DF_2005to2014 = DF_2005to2014.groupby(['Month','Day']).agg({'Max':np.max, 'Min':np.min}).reset_index()

DF_2015 = DF[DF['Year']==2015].rename(columns={'Max':'2015 Max','Min':'2015 Min'}).reset_index().drop(['index','Year','Date'], axis=1)
if len(DF_2015) != len(DF_2005to2014):
    print('data length not the same')
    
  # recombine the data
DF = pd.merge(DF_2005to2014, DF_2015, on=['Month','Day'])


# 2. Plot the Data

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15,10))

ax.fill_between(np.arange(len(DF)), DF['Max'], DF['Min'], facecolor='lightgrey')
ax.plot(DF['Max'], linewidth=0.5, c='r', label='2005~2014 Max')
ax.plot(DF['Min'], linewidth=0.5, c='b', label='2005~2014 Min')
ax.scatter(np.where(DF['2015 Max']>DF['Max'])[0], DF['2015 Max'][np.where(DF['2015 Max']>DF['Max'])[0]], c='darkred', label='2015 max exceeded record high')
ax.scatter(np.where(DF['2015 Min']<DF['Min'])[0], DF['2015 Min'][np.where(DF['2015 Min']<DF['Min'])[0]], c='darkblue', label='2015 min exceeded record low')
ax.set_xticks(np.where(DF['Day']==1)[0])
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_xlabel('Time of the Year',  fontsize=13)
ax.set_ylabel('Temperature (Celsius)', fontsize=13)
ax.legend(loc=8, frameon=False)
ax.set_title('Temperature Span Throughout The Year in 2005~2014, and Anomalies in 2015',fontsize=20)

plt.show()


fig.savefig('assignment2.png')
