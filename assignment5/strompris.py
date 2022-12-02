#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
from typing import Optional

import altair as alt
import pandas as pd
import requests
import requests_cache


# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: Optional[datetime.date] = None, location: Optional[str] = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Args:
        end_date: The desired date. Date-object using the default Python function datetime.date.
        
        Default is today's date. Only supports dates after 2 Oct 2022.

        location: Specify region to gather data from. Default key-value pair is "NO1": "Oslo / Øst-Norge".
    Returns:
        df: DataFrame with columns "NOK_per_kWh" and "time_start" in JSON.
    """

    if date is None:
        date = datetime.date.today()
    assert date > datetime.date(2022, 10, 1), "Only dates after October 2nd 2022 allowed."

    day, month = date.day, date.month
    # Zero-pads date so it works with the API
    if day < 10:
        day = "0" + str(day)
    if month < 10:
        month = "0" + str(month)


    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
    r = requests.get(url)
    assert r.status_code == 200, [r.status_code, url]

    df = pd.read_json(r.text)
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")
    #df["NOK_per_kWh"] = pd.to_numeric(df["NOK_per_kWh"])
    #df["time_start"] = pd.DatetimeIndex(df["time_start"], tz="Europe/Oslo")
    

    return df[["NOK_per_kWh", "time_start"]]

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}

# task 1:


def fetch_prices(
    end_date: Optional[datetime.date] = None,
    days: Optional[int] = 7,
    locations: Optional[tuple] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Args:
        end_date: The desired end-date. Date-object using the default Python function datetime.date.
        Default is today's date. Only supports dates after 2 Oct 2022.
        
        days: The number of days prior to the end-date to fetch. Default is 7.
        
        locations: Specify region to gather data from. Default is all regions.
    Returns:
        df: DataFrame with the desired data in JSON.
    """

    if end_date is None:
        end_date = datetime.date.today()
    
    df = pd.DataFrame()
    for i in locations:
        previous = end_date
        for j in range(days):
            
            df_day = fetch_day_prices(previous, i)
            df_day['location_code'] = i
            df_day['location'] = LOCATION_CODES[i]
            df = pd.concat([df, df_day])
            
            previous -= datetime.timedelta(days = 1)
            
    return df

def _plotter(df: pd.DataFrame, select: bool = False) -> alt.Chart:
    """Method that works under the hood that plots with Altair. 

    Args:
        df: Plots the desired chart using Altair
    Returns:
        chart |Optional[selector]: Returns the (horizontally-concatenated) alt.Chart's "selector" and "chart"
    """


    _chart = alt.Chart(df).mark_line()\
    .encode(x="time_start:T", y="NOK_per_kWh:Q",color=alt.Color('location:N',legend=None))

    if select:
        _sel = alt.selection_multi(fields=['location'])
        _make = pd.DataFrame({'location': list(LOCATION_CODES.values())})
        _selector = alt.Chart(_make).mark_rect().encode(y='location', color='location').add_selection(_sel)
        _chart = _chart.transform_filter(_sel)
        return _chart, _selector

    return _chart


def plot_prices(df: pd.DataFrame) -> alt.HConcatChart:
    """Plot energy prices over time

    Args:
        df: Plots the desired chart using Altair
    Returns:
        selector | chart: Returns the horizontally-concatenated alt.Chart's "selector" and "chart"
    """
    chart, selector = _plotter(df, select = True)
    chart = chart.properties(title=['Energy prices over time'] )
    selector = selector.properties(title=['Clicking a square dispays a single line.',\
     'Use shift-click to add more lines or double-click to display all.'])
    
    return chart | selector

# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    Args:
        df: Plots the desired chart using Altair
    Returns:
        chart: Returns the desired average chart
    
    """

    # There's probably a way to do this that's way easier...
    avg = df.groupby(['location',df['time_start'].dt.day]).mean()  
    days = len(set(df['time_start'].dt.day))
    idxs = [0]*len(avg.index)
    dates = df['time_start'].dt.date.unique()
    regions = len(set(df['location']))

    count = 0
    for i in range(regions):
        for j in range(days):
            idxs[count] = [list(sorted(LOCATION_CODES.values()))[i], list(sorted(LOCATION_CODES.keys()))[i] , dates[j], float(avg.values[count])]
            count += 1
           
    avg = pd.DataFrame(idxs, columns=["location", "location_code", "time_start", "NOK_per_kWh"])
    
    avg["time_start"] = pd.to_datetime(avg["time_start"], utc=True).dt.tz_convert("Europe/Oslo")
    
    chart = _plotter(avg)
    chart = chart.properties(title='Mean price per day')

    return  chart


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main() -> alt.Chart:
    """Allow running this module as a script for testing.
    Calls:
        df = fetch_prices(): Default values are todays date, 7 days and all regions.
        plot_prices(df): Constructs the altair.Chart from the DataFrame returned by fetch_prices()
    Returns:
        alt.Chart: Displays the chart. Requiers altair_viewer, jupyter notebook (and derivatives) or an IDE.
    """
    df = fetch_prices()
    chart = plot_daily_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
