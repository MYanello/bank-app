import csv
import io
import json
import logging
import os
from datetime import UTC, datetime

import requests

CACHE_LOCATION = "./cache/"

logger = logging.getLogger("bank-app")


def fetch_and_cache_csv(url: str, year: int, force_refresh=False):
    """Check the cache for the CSV file for the given year.

    If not found or force_refresh is True, fetch from the URL and cache it.
    """
    if not os.path.exists(CACHE_LOCATION):
        os.makedirs(CACHE_LOCATION)
    # TODO, if year > year.now then raise error
    if datetime.now(UTC).year == year:
        # Always refresh current year so we have the latest data,
        # TODO: make this a scheduled job instead to run daily
        logger.debug("Forcing refresh for current year: %s", year)
        force_refresh = True

    cache_path = CACHE_LOCATION + str(year) + ".json"
    if not force_refresh and os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            logger.debug(
                "cache hit for %s yields; cachepath: %s", year, cache_path
            )
            json_data = f.read()
    else:  # TODO: try/except the request
        logger.debug(
            "cache miss for %s yields; cachepath: %s", year, cache_path
        )
        response = requests.get(url, timeout=30)
        csvfile = io.StringIO(response.text)
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        json_data = json.dumps(rows)
        with open(cache_path, "w") as f:
            f.write(json_data)
    return json_data


def fetch_yield_data(year: int = datetime.now(UTC).year):
    base_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
    filt = f"{year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv"  # NOQA: E501
    yields_endpoint = f"{base_url}/{filt}"

    return fetch_and_cache_csv(yields_endpoint, year)
