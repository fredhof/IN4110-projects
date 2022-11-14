#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache


# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Make sure to document arguments and return value...
    ...
    """
    if date is None:
        date = datetime.date.today()
    assert date > datetime.date(2022, 10, 2), "Only dates after October 2nd 2022 allowed."

    day, month = date.day, date.month
    if date.day < 10:
        day = "0" + str(date.day)
    if date.month < 10:
        month = "0" + str(date.month)


    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
    r = requests.get(url)
    assert r.status_code == 200, [r.status_code, url]

    df = pd.read_json(r.text)
    #df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")

    return df[["NOK_per_kWh", "time_start"]]

# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo / Øst-Norge",
    "NO2": "Kristiansand / Sør-Norge",
    "NO3": "Trondheim / Midt-Norge",
    "NO4": "Tromsø / Nord-Norge",
    "NO5": "Bergen / Vest-Norge"
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value...
    ...
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

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """
   
    sel = alt.selection_multi(fields=['location'])
    make = pd.DataFrame({'location': list(LOCATION_CODES.values())})
    selector = alt.Chart(make).mark_rect().encode(y='location', color='location').add_selection(sel)
    chart = alt.Chart(df).mark_line()\
    .encode(x="time_start:T", y="NOK_per_kWh:Q",color=alt.Color('location:N',legend=None))\
    .transform_filter(sel)\
    .properties(title=['Energy prices over time.', 'Clicking a square dispays a single line.',\
     'Use shift-click to add more lines or double click to display all'])
   
    return selector | chart

# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


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


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    #main()
    df = fetch_prices(datetime.date.today(), days = 7, locations = LOCATION_CODES)
    plot_prices(df).show()
