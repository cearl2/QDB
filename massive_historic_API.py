import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from massive import RESTClient

load_dotenv()


def get_daily_aggs(
    ticker,
    start_date,
    end_date,
    adjusted=True,
    sort="asc",
    limit=50000,
):
    """Fetch daily aggregate bars for a ticker between two YYYY-MM-DD dates."""
    ticker = ticker.strip().upper()
    if not ticker:
        raise ValueError("ticker must not be empty")

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except (TypeError, ValueError) as error:
        raise ValueError("start_date and end_date must use YYYY-MM-DD format") from error

    if start > end:
        raise ValueError("start_date must be on or before end_date")
    if sort not in ("asc", "desc"):
        raise ValueError("sort must be 'asc' or 'desc'")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")

    api_key = os.getenv("massive_api")
    if not api_key:
        raise RuntimeError("Set the massive_api environment variable before fetching data")

    client = RESTClient(api_key)
    return list(
        client.list_aggs(
            ticker,
            1,
            "day",
            start.isoformat(),
            end.isoformat(),
            adjusted=adjusted,
            sort=sort,
            limit=limit,
        )
    )


def save_daily_aggs_to_json(
    ticker,
    start_date,
    end_date,
    adjusted=True,
    sort="asc",
    limit=50000,
):
    """Fetch daily aggregates, save them as timestamped JSON, and return the file path."""
    ticker = ticker.strip().upper()
    request_timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    aggs = get_daily_aggs(
        ticker,
        start_date,
        end_date,
        adjusted=adjusted,
        sort=sort,
        limit=limit,
    )
    filename = (
        f"{ticker}_1day_{start_date}_to_{end_date}_"
        f"adjusted-{str(adjusted).lower()}_sort-{sort}_limit-{limit}_"
        f"{request_timestamp}.json"
    )
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump([vars(agg) for agg in aggs], output_file, indent=2)

    print(f"Saved {len(aggs)} daily bars to {output_path}")
    return output_path


def get_daily_close_prices(ticker, start_date, end_date, adjusted=True):
    """Return daily closing prices as a {YYYY-MM-DD: close} dictionary."""
    aggs = get_daily_aggs(
        ticker,
        start_date,
        end_date,
        adjusted=adjusted,
        sort="asc",
    )
    return {
        datetime.fromtimestamp(agg.timestamp / 1000, tz=timezone.utc)
        .date()
        .isoformat(): agg.close
        for agg in aggs
    }

