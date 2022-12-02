import datetime
from typing import List, Optional
import os

import uvicorn
import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'templates')
templates = Jinja2Templates(directory=template_dir)


# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
async def root(req: Request):
    return templates.TemplateResponse("strompris.html", {"request":req, "location_codes":LOCATION_CODES, "today":datetime.date.today()})


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get("/plot_prices.json")
async def plt_prices(locations: list  = Query(list(LOCATION_CODES.keys())), end: datetime.date = datetime.date.today(), days: int = 7) -> alt.Chart.to_dict:
    df = fetch_prices(end, days, locations)
    prices = plot_prices(df)
    avg_prices = plot_daily_prices(df)
    # uncomment to test that pytest passes all tests.
    #return (avg_prices).to_dict() # PASSES. prices is HConcatChart so it will fail. So will the below line!
    return (avg_prices | prices).to_dict()



# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

#@app.get("/activity")

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)

...


# mount your docs directory as static files at `/help`
help_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'docs', '_build', 'html')
print(help_dir)
app.mount("/help", StaticFiles(directory=help_dir, html=True), name='index.html')

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000

    uvicorn.run(app, host="localhost", port=5000)
