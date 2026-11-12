import finnhub
from datetime import date

# Replace this with your actual Finnhub API key from developer.finnhub.io
API_KEY = 'YOUR_API_KEY_HERE'

def get_daily_historic_ohlcv(symbol, start_date, end_date):
    try:
        # Initialize the Client
        fh_client = finnhub.Client(api_key=API_KEY)
        
        # Define Parameters
        symbol = symbol.upper()  # API is case-insensitive but normalizing helps
        period = "1d"            # Daily candles (Open, High, Low, Close, Volume)
        resolution = "D"         # Daily resolution
        
        # Dates must be in YYYY-MM-DD format
        from_date = start_date
        to_date = end_date

        # Call the endpoint (Note: Method names may vary slightly by version of finnhub-python)
        # Standard method often used is 'get_candles' or accessing the /v2/market/candles logic.
        # If get_candlesticks is not found in your specific version, raw requests are safer.
        
        try:
            # Method name based on most recent Finnhub Python SDKs
            candles_data = fh_client.get_candlesticks(symbol=symbol, 
                                                       period=period, 
                                                       resolution=resolution, 
                                                       from_date=from_date, 
                                                       to_date=to_date)
            
            return candles_data
        except AttributeError:
            # Fallback if your library version doesn't support get_candlesticks directly.
            # This simulates the API call to ensure reliability for daily OHLC data
            import requests
            
            url = f"https://api.finnhub.io/v1/stock/{symbol}/candles"
            params = {
                'from': from_date, 
                'to': to_date, 
                'period': period, 
                'resolution': resolution
            }
            
            response = requests.get(url, headers={"X-Tokens": API_KEY}, params=params)
            raw_data = response.json()
            return raw_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# --- Execution ---
if __name__ == "__main__":
    symbol = "AAPL"  # Apple Inc.
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 15)

    data = get_daily_historic_ohlcv(symbol, str(start_date), str(end_date))

    if data:
        # Finnhub returns a list of dictionaries
        for day in data:
            print(f"Date: {day.get('time', 'N/A')}")
            open_price = day.get('o')
            high_price = day.get('h')
            low_price = day.get('l')
            close_price = day.get('c')
            print(f"  Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")