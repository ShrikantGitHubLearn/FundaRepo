import json
from os.path import abspath, dirname, join
from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


current_dir = dirname(abspath(__file__))
wellknown_path = join(current_dir, ".well-known")
historical_data = join(current_dir, "weather.json")

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=wellknown_path), name="static")


# load historical json data and serialize it:
with open(historical_data, "r") as f:
    data = json.load(f)


@app.get("/")
def root() -> RedirectResponse:
    """
    Allows to open the API documentation in the browser directly instead of
    requiring to open the /docs path.
    """
    return RedirectResponse(url="/docs", status_code=301)


@app.get("/countries")
def countries() -> list[str]:
    """Return all countries with historical weather data."""
    return list(data.keys())


@app.get("/countries/{country}/cities")
def cities(country: str) -> list[str]:
    """Return the cities with historical weather data for a country."""
    return list(data[country].keys())


@app.get("/countries/{country}/{city}/{month}")
def monthly_average(country: str, city: str, month: str) -> Any:
    """Return the historical weather data for a city's month."""
    return data[country][city][month]


# Generate the OpenAPI schema:
openapi_schema = app.openapi()
with open(join(wellknown_path, "openapi.json"), "w") as f:
    json.dump(openapi_schema, f)